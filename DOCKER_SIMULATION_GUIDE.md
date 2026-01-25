# PNGNav Docker Simulation Guide

Complete guide for running PNGNav with TurtleBot3 in Gazebo simulation using Docker.

## Prerequisites

### Windows
1. **Docker Desktop** with WSL2 backend
2. **VcXsrv** or **GWSL** for X11 display (for Gazebo GUI)
3. **NVIDIA GPU** (optional, for neural network acceleration)

### X11 Setup (Windows)
1. Install VcXsrv from: https://sourceforge.net/projects/vcxsrv/
2. Launch XLaunch with these settings:
   - Multiple windows
   - Start no client
   - **Disable access control** (checked)
   - Save configuration

## Quick Start

### 1. Build and Start Container

```powershell
# Clone the repository (if not done)
cd F:\RESEARCH
git clone https://github.com/your-repo/PNGNav.git
cd PNGNav

# Build Docker image
docker-compose build

# Start container
docker-compose up -d

# Enter container
docker-compose exec pngnav-gazebo bash
```

### 2. Build ROS2 Package (First Time Only)

Inside the container:
```bash
# Use system Python for building
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:$PATH
source /opt/ros/humble/setup.bash

# Build
cd /workspace/PNGNav
colcon build --packages-select png_navigation

# Fix Windows line endings (important if editing on Windows!)
sed -i 's/\r$//' install/png_navigation/lib/png_navigation/*.py

# Source workspace
source install/setup.bash
```

### 3. Run Simulation

You need **5 terminals**. For each new terminal, run:
```bash
docker-compose exec pngnav-gazebo bash
```

Then source the environment in each:
```bash
source /opt/ros/humble/setup.bash
source /workspace/PNGNav/install/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
```

#### Terminal 1: Gazebo
```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

#### Terminal 2: Navigation (Map + AMCL)
```bash
ros2 launch png_navigation turtlebot3_navigation.launch.py
```

Or manually specify map:
```bash
ros2 launch png_navigation turtlebot3_navigation.launch.py \
    map:=/workspace/PNGNav/src/png_navigation/src/png_navigation/maps/map_gazebo.yaml
```

#### Terminal 3: RViz
```bash
ros2 launch png_navigation rviz_navigation_static.launch.py
```

#### Terminal 4: Localize Robot (Temporary)
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```
- Use arrow keys to move the robot around
- In RViz, click **"2D Pose Estimate"** and set the robot's approximate position on the map
- Once particles converge, press **Ctrl+C** to stop teleop

#### Terminal 5: Path Planner
```bash
conda activate pngenv
ros2 launch png_navigation rrt_star.launch.py
```

Wait for: **"Global Planner is initialized."**

### 4. Set Initial Robot Pose (IMPORTANT)

Before navigation can work, you must tell AMCL where the robot is on the map:

1. **In RViz**, find the **"2D Pose Estimate"** button in the top toolbar
2. **Click the button** to activate pose estimation mode
3. **Look at Gazebo** to see where your robot actually is (note its position and which way it's facing)
4. **Click on the RViz map** at that same location where the robot is in Gazebo
5. **Drag the mouse** to set the orientation (green arrow shows which way the robot is facing - match it to Gazebo)
6. **Release** - you should see green particle clouds appear around the robot
7. **Optional**: Move the robot slightly using teleop to help AMCL converge:
   ```bash
   ros2 run turtlebot3_teleop teleop_keyboard
   ```
   Use arrow keys to move, then Ctrl+C to stop.

**How to know it worked:**
- Green particles in RViz should cluster tightly around the robot
- The robot model in RViz should align with obstacles on the map
- No more "waiting for initial pose" warnings in terminals

**Default spawn location in Gazebo**: The TurtleBot3 spawns at approximately `(x=-2.0, y=-0.5)` facing forward in `turtlebot3_world`.

### 5. Test Navigation

1. In RViz, click **"2D Goal Pose"** button
2. Click on the map where you want the robot to go and drag to set orientation
3. The robot should plan a path and navigate!

## Available Planners

| Planner | Launch Command | Description |
|---------|----------------|-------------|
| RRT* | `ros2 launch png_navigation rrt_star.launch.py` | Basic RRT* (no neural network) |
| IRRT* | `ros2 launch png_navigation irrt_star.launch.py` | Informed RRT* |
| NRRT* | `ros2 launch png_navigation nrrt_star.launch.py` | Neural RRT* |
| NIRRT* | `ros2 launch png_navigation nirrt_star.launch.py` | Neural Informed RRT* |
| NIRRT*-C | `ros2 launch png_navigation nirrt_star_c.launch.py` | NIRRT* with constraints (recommended) |

## Troubleshooting

### Gazebo not displaying
- Ensure VcXsrv/GWSL is running with "Disable access control"
- Check DISPLAY variable: `echo $DISPLAY`
- Test X11: `xclock` (should show a clock window)

### Package not found
```bash
source /opt/ros/humble/setup.bash
source /workspace/PNGNav/install/setup.bash
ros2 pkg list | grep png
```

### Build fails with Python errors
```bash
# Deactivate conda and use system Python for building
conda deactivate
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:$PATH
colcon build --packages-select png_navigation
```

### Robot not moving
```bash
# Check if cmd_vel is being published
ros2 topic echo /cmd_vel

# Check if planner is running
ros2 node list | grep planner
```

### Map not loading
```bash
# Verify map file exists
ls /workspace/PNGNav/src/png_navigation/src/png_navigation/maps/

# Check map server status
ros2 topic echo /map --once
```

### Initial pose not working / Robot not localized
- Make sure the navigation launch (Terminal 2) is running and shows "AMCL active"
- Check if the map is visible in RViz (gray/white grid with black obstacles)
- Try setting the pose multiple times - click precisely where the robot is in Gazebo
- Move the robot with teleop after setting pose to help particles converge
- Check AMCL status:
  ```bash
  ros2 topic echo /amcl_pose --once
  ```

### "Waiting for map" or "map frame does not exist"
- The navigation stack isn't fully initialized yet
- Wait a few seconds after launching navigation
- Check map server:
  ```bash
  ros2 lifecycle get /map_server
  # Should show "active"
  ```

## Container Management

```bash
# Stop container
docker-compose down

# Restart container
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after Dockerfile changes
docker-compose build --no-cache
```

## File Locations

| Item | Path |
|------|------|
| Map files | `/workspace/PNGNav/src/png_navigation/src/png_navigation/maps/` |
| Launch files | `/workspace/PNGNav/src/png_navigation/launch/` |
| Python scripts | `/workspace/PNGNav/src/png_navigation/scripts/` |
| RViz config | `/workspace/PNGNav/src/png_navigation/rviz/` |
| Model weights | `/workspace/PNGNav/src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/model_weights/` |

## Neural Network Setup (for NIRRT*/NRRT*)

1. Download PointNet++ weights from: [Google Drive Link](https://drive.google.com/file/d/1YfocGh1pcr_Eg8XhEAxmwaAZQsosjRhM/view)
2. Place in: `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/model_weights/pointnet2_sem_seg_msg_pathplan.pth`
