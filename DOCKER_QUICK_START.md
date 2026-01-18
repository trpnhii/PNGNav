# Docker Quick Start Guide

## One-Command Setup

```bash
# Build and run
docker-compose up --build -d
docker-compose exec pngnav-gazebo bash
```

## Inside Container - Run Simulation

### Terminal 1: Gazebo
```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

### Terminal 2: Map Server & AMCL
```bash
# Open new terminal
docker-compose exec pngnav-gazebo bash

# Map server
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=/workspace/PNGNav/src/png_navigation/src/png_navigation/maps/map_gazebo.yaml

# AMCL (in another terminal)
docker-compose exec pngnav-gazebo bash
ros2 launch nav2_bringup amcl.launch.py
```

### Terminal 3: RViz
```bash
docker-compose exec pngnav-gazebo bash
ros2 run rviz2 rviz2 -d /workspace/PNGNav/src/png_navigation/rviz/navigation_static.rviz
```

### Terminal 4: Path Planning
```bash
docker-compose exec pngnav-gazebo bash
python3 src/png_navigation/scripts/nirrt_star_node.py &
python3 src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --use_neural_wrapper --map map_gazebo
```

## Common Commands

```bash
# Build
docker-compose build

# Start container
docker-compose up -d

# Enter container
docker-compose exec pngnav-gazebo bash

# Stop container
docker-compose down

# View logs
docker-compose logs -f

# Rebuild (after dependency changes)
docker-compose build --no-cache
```

## Fix X11 (for GUI)

```bash
# Linux
xhost +local:docker

# Then restart container
docker-compose restart
```

## Full Documentation

See `DOCKER_SETUP.md` for detailed instructions.
