# Go to workspace root (parent of src folder)
cd /workspace/PNGNav

# Source ROS2
source /opt/ros/humble/setup.bash

# Build the package
colcon build --packages-select png_navigation --symlink-install

# Source the workspace
source install/setup.bash