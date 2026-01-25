# Running PNGNav with Gazebo Simulation (ROS2)

This guide provides step-by-step instructions to run the ROS2-converted PNGNav package with TurtleBot3 in Gazebo simulation.

## Prerequisites

### 1. Install ROS2
Choose your ROS2 distribution:
- **ROS2 Humble** (Ubuntu 22.04)
- **ROS2 Foxy** (Ubuntu 20.04)

```bash
# For ROS2 Humble (Ubuntu 22.04)
sudo apt update
sudo apt install ros-humble-desktop

# For ROS2 Foxy (Ubuntu 20.04)
sudo apt update
sudo apt install ros-foxy-desktop
```

### 2. Install TurtleBot3 ROS2 Packages

```bash
# For ROS2 Humble
sudo apt install ros-humble-turtlebot3*
sudo apt install ros-humble-turtlebot3-gazebo
sudo apt install ros-humble-turtlebot3-navigation2
sudo apt install ros-humble-nav2-bringup

# For ROS2 Foxy
sudo apt install ros-foxy-turtlebot3*
sudo apt install ros-foxy-turtlebot3-gazebo
sudo apt install ros-foxy-turtlebot3-navigation2
sudo apt install ros-foxy-nav2-bringup
```

### 3. Set Environment Variables

Add to `~/.bashrc`:
```bash
# ROS2 setup (choose one based on your distribution)
source /opt/ros/humble/setup.bash  # or foxy

# TurtleBot3 model
export TURTLEBOT3_MODEL=waffle_pi

# Gazebo model path
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models
```

Then reload:
```bash
source ~/.bashrc
```

### 4. Build the Package

Since the code is ROS2, you need to build it as an ament package. However, the `package.xml` still needs to be converted to ROS2 format. For now, you can run the nodes directly:

```bash
cd ~/PNGNav
conda activate pngenv  # or your environment name
```

## Step-by-Step: Running with Gazebo

### Step 1: Launch Gazebo Simulation

**Terminal 1:**
```bash
source /opt/ros/humble/setup.bash  # or foxy
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

This will:
- Start Gazebo with the TurtleBot3 world
- Spawn a TurtleBot3 robot
- Start the robot state publisher and joint state publisher

### Step 2: Launch Navigation Stack (Map Server + AMCL)

**Terminal 2:**
```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi

# First, find your map file path
# It should be in: ~/PNGNav/src/png_navigation/src/png_navigation/maps/map_gazebo.yaml

# Launch map server
ros2 run nav2_map_server map_server \
    --ros-args \
    -p yaml_filename:=$HOME/PNGNav/src/png_navigation/src/png_navigation/maps/map_gazebo.yaml

# In a separate terminal (Terminal 2b), launch AMCL
ros2 launch nav2_bringup amcl.launch.py
```

**Alternative:** If you have a custom launch file for map server and AMCL, use that instead.

### Step 3: Launch RViz2

**Terminal 3:**
```bash
source /opt/ros/humble/setup.bash
ros2 run rviz2 rviz2 -d ~/PNGNav/src/png_navigation/rviz/navigation_static.rviz
```

Or use the ROS2 launch file:
```bash
source /opt/ros/humble/setup.bash
ros2 launch png_navigation rviz_navigation_static.launch.py
```

### Step 4: Initialize Robot Pose (Teleoperation)

**Terminal 4:**
```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 run turtlebot3_teleop teleop_keyboard
```

**Instructions:**
- Use arrow keys to move the robot
- Drive the robot around to help AMCL localize it
- Press `2D Pose Estimate` in RViz and click on the map where the robot is
- Once localized, **stop the teleop** (Ctrl+C)

### Step 5: Launch Path Planning Nodes

**Terminal 5:**
```bash
cd ~/PNGNav
source /opt/ros/humble/setup.bash
conda activate pngenv

# Option A: Using ROS2 launch files (if converted)
ros2 launch png_navigation nirrt_star_c.launch.py map:=map_gazebo

# Option B: Manual node launching (more reliable for now)
# For NIRRT* with neural wrapper (recommended):
python3 src/png_navigation/scripts/nirrt_star_node.py &
python3 src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --use_neural_wrapper --map map_gazebo

# For RRT* (simpler, no neural network):
python3 src/png_navigation/scripts/rrt_star_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --map map_gazebo

# For IRRT*:
python3 src/png_navigation/scripts/irrt_star_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --map map_gazebo

# For NRRT*:
python3 src/png_navigation/scripts/nrrt_star_node.py &
python3 src/png_navigation/scripts/nrrt_star_neural_wrapper_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --use_neural_wrapper --map map_gazebo
```

**Wait for:** `Global Planner is initialized.` message

### Step 6: Test Navigation

1. In RViz2, click **"2D Goal Pose"** button
2. Click on the map where you want the robot to go
3. The robot should plan a path and start moving

## Quick Launch Script (All-in-One)

Create a script to launch everything at once:

```bash
#!/bin/bash
# save as: launch_gazebo_test.sh

source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi

# Terminal 1: Gazebo
gnome-terminal -- bash -c "ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py; exec bash"

sleep 5

# Terminal 2: Map Server
gnome-terminal -- bash -c "ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=$HOME/PNGNav/src/png_navigation/src/png_navigation/maps/map_gazebo.yaml; exec bash"

sleep 2

# Terminal 3: AMCL
gnome-terminal -- bash -c "ros2 launch nav2_bringup amcl.launch.py; exec bash"

sleep 2

# Terminal 4: RViz
gnome-terminal -- bash -c "ros2 run rviz2 rviz2 -d ~/PNGNav/src/png_navigation/rviz/navigation_static.rviz; exec bash"

sleep 2

# Terminal 5: Path Planning Nodes
cd ~/PNGNav
source /opt/ros/humble/setup.bash
conda activate pngenv
python3 src/png_navigation/scripts/nirrt_star_node.py &
python3 src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py &
python3 src/png_navigation/scripts/local_planner_clock.py &
python3 src/png_navigation/scripts/local_planner_node.py &
python3 src/png_navigation/scripts/global_planner_node.py --use_neural_wrapper --map map_gazebo
```

## Troubleshooting

### Issue: "Package not found" errors
- Make sure you've sourced ROS2: `source /opt/ros/humble/setup.bash`
- Check that TurtleBot3 packages are installed: `ros2 pkg list | grep turtlebot3`

### Issue: Nodes not starting
- Check Python path: `echo $PYTHONPATH`
- Activate conda environment: `conda activate pngenv`
- Check node permissions: `chmod +x src/png_navigation/scripts/*.py`

### Issue: TF2 errors
- Install TF2: `sudo apt install ros-humble-tf2-ros ros-humble-tf2-tools`
- Check transforms: `ros2 run tf2_ros tf2_echo /map /base_footprint`

### Issue: Map not loading
- Verify map file exists: `ls ~/PNGNav/src/png_navigation/src/png_navigation/maps/`
- Check map server is running: `ros2 topic list | grep map`

### Issue: Robot not moving
- Check cmd_vel topic: `ros2 topic echo /cmd_vel`
- Verify local planner is running: `ros2 node list | grep local_planner`
- Check for errors in terminal output

### Issue: Service calls failing
- Verify services are available: `ros2 service list | grep png_navigation`
- Check service types: `ros2 service type /png_navigation/get_global_plan`

## Testing Individual Components

### Test a single node:
```bash
source /opt/ros/humble/setup.bash
conda activate pngenv
python3 src/png_navigation/scripts/rrt_star_node.py
```

### Check topics:
```bash
ros2 topic list
ros2 topic echo /png_navigation/get_global_plan
```

### Check services:
```bash
ros2 service list
ros2 service type /png_navigation/set_env_2d
```

## Next Steps

1. **Convert package.xml**: Update to ROS2 ament format
2. **Convert CMakeLists.txt**: Update to ament_cmake (if needed)
3. **Build with colcon**: Once package.xml is converted, use `colcon build`
4. **Create comprehensive launch files**: Combine all nodes into single launch files

## Notes

- The Python nodes are ROS2-compatible (using `rclpy`)
- Launch files are being converted to ROS2 Python format (`.launch.py`)
- For now, manual node launching is most reliable
- Make sure all dependencies (tf2_ros, nav_msgs, etc.) are installed for ROS2
