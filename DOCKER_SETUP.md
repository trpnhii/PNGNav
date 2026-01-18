# Docker Setup for PNGNav ROS2 Gazebo Simulation

This guide explains how to build and run the PNGNav simulation environment using Docker.

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)
- X11 server running (for GUI applications like Gazebo and RViz)
- NVIDIA GPU with drivers (optional, for neural network acceleration)

## Quick Start

### 1. Build the Docker Image

```bash
docker-compose build
```

Or using Docker directly:

```bash
docker build -t pngnav:ros2-gazebo .
```

### 2. Run the Container

```bash
docker-compose up -d
docker-compose exec pngnav-gazebo bash
```

Or using Docker directly:

```bash
# Allow X11 connections (Linux)
xhost +local:docker

# Run container
docker run -it \
    --network host \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/workspace/PNGNav \
    pngnav:ros2-gazebo
```

### 3. Inside the Container

The container automatically:
- Sources ROS2 Humble
- Activates the conda environment (`pngenv`)
- Sets up environment variables
- Changes to `/workspace/PNGNav`

You can now run the simulation:

```bash
# Terminal 1: Gazebo
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2: Map Server & AMCL (in new terminal)
docker-compose exec pngnav-gazebo bash
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=/workspace/PNGNav/src/png_navigation/src/png_navigation/maps/map_gazebo.yaml

# Terminal 3: RViz
docker-compose exec pngnav-gazebo bash
ros2 run rviz2 rviz2 -d /workspace/PNGNav/src/png_navigation/rviz/navigation_static.rviz

# Terminal 4: Path Planning Nodes
docker-compose exec pngnav-gazebo bash
python3 src/png_navigation/scripts/nirrt_star_node.py &
python3 src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --use_neural_wrapper --map map_gazebo
```

## Detailed Instructions

### Building the Image

The Dockerfile will:
1. Use ROS2 Humble base image
2. Install all ROS2 and TurtleBot3 packages
3. Install Miniconda
4. Create conda environment from `environment.yml`
5. Copy your code
6. Set up environment variables
7. Make scripts executable

**Build time:** ~15-30 minutes (depending on internet speed)

### Running Multiple Terminals

Since you need multiple terminals for the simulation, you can:

**Option 1: Use docker-compose exec (Recommended)**
```bash
# Open multiple terminals and run:
docker-compose exec pngnav-gazebo bash
```

**Option 2: Use tmux/screen inside container**
```bash
docker-compose exec pngnav-gazebo bash
# Inside container:
tmux new -s simulation
# Split panes: Ctrl+B then %
```

**Option 3: Use separate containers**
Modify `docker-compose.yml` to create multiple services.

### X11 Forwarding (GUI Applications)

For Gazebo and RViz to work, you need X11 forwarding:

**Linux:**
```bash
xhost +local:docker
```

**macOS:**
Install XQuartz and run:
```bash
xhost + 127.0.0.1
docker run -e DISPLAY=host.docker.internal:0 ...
```

**Windows:**
See `WINDOWS_X11_SETUP.md` for detailed instructions. Quick setup:
1. Install VcXsrv (X server for Windows)
2. Start VcXsrv with "Disable access control" enabled
3. Update `docker-compose.yml` with your Windows IP:
   ```yaml
   environment:
     - DISPLAY=YOUR_IP_ADDRESS:0.0
   ```
4. Allow VcXsrv through Windows Firewall

**Windows (WSL2):**
```bash
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
```

### GPU Support (Optional)

If you have an NVIDIA GPU and want to use it for the neural network:

1. Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

2. Modify `docker-compose.yml`:
```yaml
services:
  pngnav-gazebo:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

3. Rebuild and run:
```bash
docker-compose up --build
```

### Volume Mounts

The `docker-compose.yml` mounts:
- `./:/workspace/PNGNav` - Your code (changes reflect immediately)
- `conda-env:/opt/conda/envs` - Conda environments (persisted between rebuilds)

### Network Mode

Using `network_mode: host` allows:
- ROS2 nodes to communicate easily
- No port mapping needed
- Direct access to host network

## Common Issues

### Issue: "Cannot connect to X server"

**Solution:**
```bash
# Linux
xhost +local:docker

# Check DISPLAY
echo $DISPLAY
```

### Issue: "Permission denied" on scripts

**Solution:**
```bash
# Inside container
chmod +x src/png_navigation/scripts/*.py
```

### Issue: "Package not found" errors

**Solution:**
```bash
# Inside container, verify ROS2 is sourced
source /opt/ros/humble/setup.bash
ros2 pkg list | grep turtlebot3
```

### Issue: Conda environment not activating

**Solution:**
```bash
# Manually activate
eval "$(conda shell.bash hook)"
conda activate pngenv
```

### Issue: Slow Gazebo startup

**Solution:**
- Use `--headless` mode for Gazebo (no GUI)
- Reduce simulation quality in Gazebo settings
- Allocate more resources to Docker

## Updating the Image

If you change `environment.yml` or dependencies:

```bash
# Rebuild
docker-compose build --no-cache

# Or rebuild specific stage
docker build --target <stage> -t pngnav:ros2-gazebo .
```

## Cleaning Up

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi pngnav:ros2-gazebo

# Remove volumes (WARNING: deletes conda env)
docker-compose down -v
```

## Development Workflow

1. **Edit code on host** - Changes are immediately available in container
2. **Test in container** - Run nodes inside container
3. **Rebuild only when dependencies change** - Use `docker-compose build`

## Tips

- Use `docker-compose exec` to open new terminals
- Keep the container running in background: `docker-compose up -d`
- View logs: `docker-compose logs -f`
- Use `--rm` flag for temporary containers
- Mount only what you need to speed up builds

## Next Steps

Once the container is running, follow the instructions in `GAZEBO_ROS2_TESTING.md` or `QUICK_START_GAZEBO.md` for running the simulation.
