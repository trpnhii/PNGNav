cmake_minimum_required(VERSION 3.8)
project(png_navigation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate messages and services
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/NavigationEnvMsg.msg"
  "msg/NavigationProblem.msg"
  "msg/NIRRTWrapperMsg.msg"
  "srv/SetEnv.srv"
  "srv/GetGlobalPlan.srv"
  "srv/GlobalReplan.srv"
  "srv/StopRobot.srv"
  "srv/ResumeRobot.srv"
  DEPENDENCIES std_msgs geometry_msgs
)

# Install Python scripts as executables
install(PROGRAMS
  scripts/global_planner_node.py
  scripts/irrt_star_node.py
  scripts/local_planner_clock.py
  scripts/local_planner_node.py
  scripts/nirrt_star_c_neural_wrapper_node.py
  scripts/nirrt_star_neural_wrapper_node.py
  scripts/nirrt_star_node.py
  scripts/nrrt_star_neural_wrapper_node.py
  scripts/nrrt_star_node.py
  scripts/rrt_star_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python source modules to lib/python site-packages
install(DIRECTORY
  src/${PROJECT_NAME}/
  DESTINATION lib/python3/dist-packages/${PROJECT_NAME}
  PATTERN "__pycache__" EXCLUDE
  PATTERN "*.pyc" EXCLUDE
)

# Install launch files
install(DIRECTORY
  launch/
  DESTINATION share/${PROJECT_NAME}/launch
  PATTERN "*.launch" EXCLUDE
)

# Install dynamic obstacles launch files  
install(DIRECTORY
  launch_dynamic_obstacles/
  DESTINATION share/${PROJECT_NAME}/launch_dynamic_obstacles
  PATTERN "*.launch" EXCLUDE
)

# Install rviz configs
install(DIRECTORY
  rviz/
  DESTINATION share/${PROJECT_NAME}/rviz
)

# Install maps
install(DIRECTORY
  src/${PROJECT_NAME}/maps/
  DESTINATION share/${PROJECT_NAME}/maps
)

# Install package.xml explicitly
install(FILES
  package.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
