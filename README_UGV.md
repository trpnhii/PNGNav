# PNGNav ROS2 UGV Deployment Guide

This guide covers how to run the NIRRT*-PNG navigation algorithm on a real UGV (Unmanned Ground Vehicle) using ROS2 Humble in Docker.

## Prerequisites

- Docker Desktop installed on your system
- UGV with ROS2 Humble running
- X11 server for GUI (VcXsrv or GWSL on Windows)

## Quick Start

### 1. Build the Docker Container

```bash
cd /path/to/PNGNav

# Build without GPU
docker-compose -f docker-compose.ugv-nogpu.yml build

# Or build with GPU (if you have NVIDIA GPU)
docker-compose -f docker-compose.ugv.yml build
```

### 2. Start the Container

```bash
# Start without GPU
docker-compose -f docker-compose.ugv-nogpu.yml up -d

# Or start with GPU
docker-compose -f docker-compose.ugv.yml up -d
```

### 3. Enter the Container

```bash
docker exec -it pngnav-ugv-ros2 bash
```

---

## Building the ROS2 Package

Inside the container, the package must be built using **system Python** (not conda):

```bash
# 1. Remove conda from PATH to use system Python
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 2. Verify system Python is used
which python3
# Should show: /usr/bin/python3

# 3. Install required Python packages (if not already installed)
/usr/bin/pip3 install empy==3.3.4 lark catkin_pkg

# 4. Source ROS2
source /opt/ros/humble/setup.bash

# 5. Unset RMW (use default FastDDS)
unset RMW_IMPLEMENTATION

# 6. Clean and build
cd /workspace/PNGNav
rm -rf build/ install/ log/
colcon build --packages-select png_navigation

# 7. Source the package
source install/setup.bash
```

---

## Verifying ROS2 Setup

### Check ROS2 Installation

```bash
ros2 --version
ros2 pkg list | grep png
ros2 pkg executables png_navigation
```

### Check Available Topics

```bash
ros2 topic list
```

### Check Available Services

```bash
ros2 service list
```

---

## Running the Navigation Algorithm

### Terminal Setup for Running Nodes

When running the actual nodes (which need PyTorch), activate conda:

```bash
# Add conda to PATH
export PATH=/opt/conda/bin:$PATH
conda activate pngenv

# Source ROS2 and package
source /opt/ros/humble/setup.bash
source /workspace/PNGNav/install/setup.bash
unset RMW_IMPLEMENTATION
```

### Available Planning Algorithms

| Algorithm | Launch Command |
|-----------|----------------|
| RRT* | `ros2 launch png_navigation rrt_star.launch.py` |
| Informed RRT* | `ros2 launch png_navigation irrt_star.launch.py` |
| Neural RRT* | `ros2 launch png_navigation nrrt_star.launch.py` |
| NIRRT* | `ros2 launch png_navigation nirrt_star.launch.py` |
| NIRRT*-C (Recommended) | `ros2 launch png_navigation nirrt_star_c.launch.py` |

### Running with Custom Map

```bash
ros2 launch png_navigation nirrt_star_c.launch.py map:=your_map_name
```

---

## UGV Integration Requirements

### Required Topics from UGV

Your UGV must publish these topics:

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `/odom` | `nav_msgs/msg/Odometry` | Robot odometry |
| `/scan` | `sensor_msgs/msg/LaserScan` | Lidar data |
| `/tf` | `tf2_msgs/msg/TFMessage` | Transform tree |

### Required Topics to UGV

The planner publishes velocity commands to:

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Velocity commands |

### Verify UGV Topics

```bash
# Check if UGV topics are available
ros2 topic list

# Test odometry
ros2 topic echo /odom --once

# Test lidar
ros2 topic echo /scan --once

# Check TF tree
ros2 run tf2_tools view_frames
```

---

## Multi-Terminal Setup for Full System

### Terminal 1: Launch Navigation Stack

```bash
docker exec -it pngnav-ugv-ros2 bash

export PATH=/opt/conda/bin:$PATH
conda activate pngenv
source /opt/ros/humble/setup.bash
source /workspace/PNGNav/install/setup.bash
unset RMW_IMPLEMENTATION

ros2 launch png_navigation nirrt_star_c.launch.py
```

### Terminal 2: Monitor Topics

```bash
docker exec -it pngnav-ugv-ros2 bash

source /opt/ros/humble/setup.bash
source /workspace/PNGNav/install/setup.bash

# Watch planning services
ros2 service list | grep png_navigation

# Monitor cmd_vel output
ros2 topic echo /cmd_vel
```

### Terminal 3: RViz Visualization (Optional)

```bash
docker exec -it pngnav-ugv-ros2 bash

source /opt/ros/humble/setup.bash
source /workspace/PNGNav/install/setup.bash

ros2 launch png_navigation rviz_navigation_static.launch.py
```

---

## Diagnostic Script

Save this as `diagnose.sh` and run it to check your setup:

```bash
#!/bin/bash
echo "=== ROS2 Version ==="
ros2 --version 2>/dev/null || echo "ROS2 not available"

echo -e "\n=== PNG Navigation Package ==="
ros2 pkg list 2>/dev/null | grep png || echo "Package not found!"

echo -e "\n=== Available Executables ==="
ros2 pkg executables png_navigation 2>/dev/null || echo "No executables found"

echo -e "\n=== Active Topics ==="
ros2 topic list 2>/dev/null || echo "No topics"

echo -e "\n=== Active Services ==="
ros2 service list 2>/dev/null | grep png || echo "No PNG services"

echo -e "\n=== Python Check ==="
python3 -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>/dev/null || echo "PyTorch not available"
python3 -c "import rclpy; print('rclpy: OK')" 2>/dev/null || echo "rclpy not available"

echo -e "\n=== TF Frames ==="
ros2 run tf2_ros tf2_echo odom base_link 2>/dev/null &
sleep 2
kill $! 2>/dev/null
```

---

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'em'`

The build is using conda Python instead of system Python. Fix:

```bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
/usr/bin/pip3 install empy==3.3.4 lark catkin_pkg
```

### Error: `failed to load shared library 'librmw_cyclonedds_cpp.so'`

CycloneDDS is not installed. Use default FastDDS:

```bash
unset RMW_IMPLEMENTATION
```

### Error: `exec format error` during Docker build

Architecture mismatch. The base image may not match your system architecture.

### Nodes not finding each other

Ensure all terminals have the same ROS_DOMAIN_ID:

```bash
export ROS_DOMAIN_ID=0
```

### GUI not working (RViz/Gazebo)

1. Start X11 server (VcXsrv/GWSL) on Windows
2. Set DISPLAY variable:

```bash
export DISPLAY=host.docker.internal:0.0
```

---

## File Structure

```
PNGNav/
├── docker-compose.ugv.yml          # Docker Compose with GPU
├── docker-compose.ugv-nogpu.yml    # Docker Compose without GPU
├── Dockerfile.ugv                  # Dockerfile for UGV
├── src/
│   └── png_navigation/
│       ├── launch/                 # ROS2 launch files
│       │   ├── rrt_star.launch.py
│       │   ├── irrt_star.launch.py
│       │   ├── nrrt_star.launch.py
│       │   ├── nirrt_star.launch.py
│       │   └── nirrt_star_c.launch.py
│       ├── scripts/                # Python nodes
│       │   ├── global_planner_node.py
│       │   ├── local_planner_node.py
│       │   ├── rrt_star_node.py
│       │   └── ...
│       └── src/png_navigation/     # Python library
└── README_UGV.md                   # This file
```

---

## References

- [NIRRT*-PNG Paper (ICRA 2024)](https://ieeexplore.ieee.org/abstract/document/10611099)
- [Main GitHub Repository](https://github.com/tedhuang96/nirrt_star)
- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
