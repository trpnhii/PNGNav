ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py


source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi

# Launch the TurtleBot3 navigation (includes map server + AMCL)
ros2 launch png_navigation turtlebot3_navigation.launch.py



# Terminal 2: Launch navigation (map server + AMCL)
ros2 launch png_navigation turtlebot3_navigation.launch.py

# Terminal 3: Launch RViz
ros2 launch png_navigation rviz_navigation_static.launch.py

# Terminal 4: Teleop (temporary, for localization)
ros2 run turtlebot3_teleop teleop_keyboard

# Terminal 5: Launch planner
conda activate pngenv
ros2 launch png_navigation rrt_star.launch.py




#############################
### BUILD ###################
# Clean everything completely
cd /workspace/PNGNav
rm -rf build/ install/ log/

# Also remove any CMake cache in the source directory
rm -rf src/png_navigation/CMakeFiles/
rm -f src/png_navigation/CMakeCache.txt

# Rebuild
cd /workspace/PNGNav
source /opt/ros/humble/setup.bash
colcon build --packages-select png_navigation

# Source the updated workspace
source install/setup.bash

# Try again
ros2 launch png_navigation turtlebot3_navigation.launch.py



#############################
### FIX WINDOWS NEWLINE #####
# Convert line endings for all Python scripts
cd /workspace/PNGNav/install/png_navigation/lib/png_navigation/
sed -i 's/\r$//' *.py

# Also fix source scripts for future builds
cd /workspace/PNGNav/src/png_navigation/scripts/
sed -i 's/\r$//' *.py
