#!/bin/bash
# PNGNav ROS2 Diagnostic Script
# Run this inside the Docker container to verify setup

echo "========================================"
echo "  PNGNav ROS2 Diagnostic Report"
echo "========================================"

echo -e "\n=== System Info ==="
uname -a

echo -e "\n=== ROS2 Version ==="
ros2 --version 2>/dev/null || echo "ERROR: ROS2 not available or RMW issue"

echo -e "\n=== ROS Environment ==="
echo "ROS_DISTRO: $ROS_DISTRO"
echo "ROS_DOMAIN_ID: $ROS_DOMAIN_ID"
echo "RMW_IMPLEMENTATION: ${RMW_IMPLEMENTATION:-'(default)'}"

echo -e "\n=== Python Path ==="
which python3
python3 --version

echo -e "\n=== PNG Navigation Package ==="
ros2 pkg list 2>/dev/null | grep png || echo "WARNING: Package not found!"

echo -e "\n=== Available Executables ==="
ros2 pkg executables png_navigation 2>/dev/null || echo "WARNING: No executables found"

echo -e "\n=== Active Topics ==="
ros2 topic list 2>/dev/null || echo "No topics available"

echo -e "\n=== Active Services ==="
ros2 service list 2>/dev/null | grep png || echo "No PNG services running"

echo -e "\n=== Required Topics Check ==="
for topic in /odom /scan /cmd_vel /tf; do
    if ros2 topic list 2>/dev/null | grep -q "^${topic}$"; then
        echo "  [OK] $topic"
    else
        echo "  [MISSING] $topic"
    fi
done

echo -e "\n=== Python Dependencies ==="
python3 -c "import torch; print(f'  PyTorch: {torch.__version__}')" 2>/dev/null || echo "  [MISSING] PyTorch"
python3 -c "import numpy; print(f'  NumPy: {numpy.__version__}')" 2>/dev/null || echo "  [MISSING] NumPy"
python3 -c "import cv2; print(f'  OpenCV: {cv2.__version__}')" 2>/dev/null || echo "  [MISSING] OpenCV"
python3 -c "import rclpy; print('  rclpy: OK')" 2>/dev/null || echo "  [MISSING] rclpy"
python3 -c "import open3d; print(f'  Open3D: {open3d.__version__}')" 2>/dev/null || echo "  [MISSING] Open3D"

echo -e "\n=== Conda Environment ==="
if command -v conda &> /dev/null; then
    conda info --envs 2>/dev/null | head -10
else
    echo "Conda not in PATH"
fi

echo -e "\n========================================"
echo "  Diagnostic Complete"
echo "========================================"
