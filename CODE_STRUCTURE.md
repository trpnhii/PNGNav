# PNG Navigation Code Structure - Independent Parts

**Organization**: Files are grouped into parts where:

-   **No two parts depend on each other**
-   Files within the same part can depend on each other
-   Each part is completely independent

---

## Part 1: Core Utilities (Base Layer)

**Purpose**: Fundamental utilities with no dependencies on other parts

**ROS2 Compatibility**: ✅ Already ROS2 compatible - These files contain pure Python/NumPy/matplotlib code with no ROS dependencies, making them compatible with both ROS1 and ROS2.

-   `src/png_navigation/src/png_navigation/path_planning_classes/collision_check_utils.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_env_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_visualizer_2d.py`

---

## Part 2: Configuration

**Purpose**: Configuration classes (standalone)

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python configuration class with no ROS dependencies. The `ros_config` section contains topic and frame names as strings, which are compatible with both ROS1 and ROS2.

-   `src/png_navigation/src/png_navigation/configs/rrt_star_config.py`

---

## Part 3: Path Planning Utilities Wrapper

**Purpose**: Wrapper around core utilities

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python utility class with no ROS dependencies. Only imports from Part 1 (collision_check_utils) and uses NumPy.

-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_utils_2d.py`
    -   Uses: Part 1 (collision_check_utils)

---

## Part 4: Path Planning Algorithms

**Purpose**: All RRT algorithm implementations

**ROS2 Compatibility**: ❌ Needs ROS2 conversion - Uses `rospy` for publishers/subscribers in `rrt_star_2d.py`, `irrt_star_2d.py`, `nrrt_star_png_2d.py`, and `nirrt_star_png_2d.py`. `rrt_base_2d.py` is ROS2 compatible (no ROS dependencies).

-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_base_2d.py` (✅ ROS2 compatible)
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_star_2d.py` (❌ uses rospy)
-   `src/png_navigation/src/png_navigation/path_planning_classes/irrt_star_2d.py` (❌ uses rospy)
-   `src/png_navigation/src/png_navigation/path_planning_classes/nrrt_star_png_2d.py` (❌ uses rospy)
-   `src/png_navigation/src/png_navigation/path_planning_classes/nirrt_star_png_2d.py` (❌ uses rospy)
    -   Uses: Part 1 (rrt_utils_2d, rrt_visualizer_2d), Part 3 (rrt_utils_2d)

---

## Part 5: Map Utilities

**Purpose**: Map processing and coordinate transformation

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python/NumPy code with no ROS dependencies.

-   `src/png_navigation/src/png_navigation/maps/map_utils.py`
    -   Uses: Part 1 (collision_check_utils)

---

## Part 6: Point Cloud Utilities

**Purpose**: Point cloud generation and processing

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python/NumPy/Open3D code with no ROS dependencies.

-   `src/png_navigation/src/png_navigation/datasets/point_cloud_mask_utils_updated.py`
    -   Uses: Part 1 (collision_check_utils)

---

## Part 7: Neural Network Base Utilities

**Purpose**: Base neural network utilities (standalone)

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python/PyTorch/NumPy code with no ROS dependencies.

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/models/pointnet2_utils.py`
-   `src/png_navigation/src/png_navigation/wrapper/utils/bfs_connect_heuristic.py`

---

## Part 8: Neural Network Models

**Purpose**: Neural network model definitions

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure PyTorch model definition with no ROS dependencies.

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/models/pointnet2_sem_seg_msg_pathplan.py`
    -   Uses: Part 7 (pointnet2_utils)

---

## Part 9: Neural Network Wrapper

**Purpose**: Main neural network wrapper class

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python/PyTorch code with no ROS dependencies.

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/pointnet2_wrapper.py`
    -   Uses: Part 7 (pointnet2_utils), Part 8 (models)

---

## Part 10: Neural Network Wrapper with BFS

**Purpose**: Neural network wrapper with BFS connection heuristic

**ROS2 Compatibility**: ✅ Already ROS2 compatible - Pure Python/PyTorch code with no ROS dependencies.

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/pointnet2_wrapper_connect_bfs.py`
    -   Uses: Part 6 (point_cloud_mask_utils), Part 7 (pointnet2_utils, bfs_connect_heuristic), Part 8 (models)

---

## Part 11: ROS Path Planning Service Nodes

**Purpose**: ROS service nodes for path planning algorithms

**ROS2 Compatibility**: ❌ Needs ROS2 conversion - All files use `rospy` for ROS1 services and nodes. Need to convert to `rclpy` for ROS2.

-   `src/png_navigation/scripts/rrt_star_node.py` (❌ uses rospy)
-   `src/png_navigation/scripts/irrt_star_node.py` (❌ uses rospy)
-   `src/png_navigation/scripts/nrrt_star_node.py` (❌ uses rospy)
-   `src/png_navigation/scripts/nirrt_star_node.py` (❌ uses rospy)
    -   Uses: Part 1 (rrt_env_2d), Part 2 (config), Part 4 (algorithms)

---

## Part 12: Global Planner

**Purpose**: High-level navigation planner

**ROS2 Compatibility**: ✅ Converted to ROS2 compatible (2025-12-19 19:24:55) - Converted from `rospy` to `rclpy`, `rospkg` to `ament_index_python`, and `tf` to `tf2_ros`. The `GlobalPlanner` class now inherits from `rclpy.node.Node`, uses ROS2 publishers/subscribers/services, and TF2 transforms.

-   `src/png_navigation/scripts/global_planner_node.py` (✅ converted to ROS2 - uses rclpy, ament_index_python, tf2_ros)
    -   Uses: Part 1 (rrt_env_2d), Part 2 (config), Part 5 (map_utils)
    -   **Changes**:
        -   Replaced `rospy` with `rclpy` and `rclpy.node.Node`
        -   Replaced `rospkg.RosPack()` with `ament_index_python.packages.get_package_share_directory()`
        -   Replaced `tf.TransformListener()` with `tf2_ros.TransformListener()` and `tf2_ros.Buffer()`
        -   Converted `rospy.Publisher` to `node.create_publisher()` with QoS profiles
        -   Converted `rospy.Subscriber` to `node.create_subscription()`
        -   Converted `rospy.ServiceProxy` to `node.create_client()` with async calls
        -   Updated time handling: `rospy.Time.now()` → `node.get_clock().now()`
        -   Updated logging: `rospy.loginfo()` → `node.get_logger().info()`
        -   Updated TF transforms to use `tf2_ros` API
        -   Replaced `tf.transformations` with `tf_transformations`

---

## Part 13: Local Planner

**Purpose**: Low-level robot control (standalone ROS node)

**ROS2 Compatibility**: ✅ Converted to ROS2 compatible (2025-12-19 19:36:51) - Converted from `rospy` to `rclpy` and `tf` to `tf2_ros`. The `LocalPlanner` class now inherits from `rclpy.node.Node`, uses ROS2 publishers/subscribers, and TF2 transforms. The `local_planner_clock.py` now uses ROS2 timer-based publishing.

-   `src/png_navigation/scripts/local_planner_node.py` (✅ converted to ROS2 - uses rclpy, tf2_ros)
-   `src/png_navigation/scripts/local_planner_clock.py` (✅ converted to ROS2 - uses rclpy)
    -   **Changes**:
        -   Replaced `rospy` with `rclpy` and `rclpy.node.Node`
        -   Replaced `tf.TransformListener()` with `tf2_ros.TransformListener()` and `tf2_ros.Buffer()`
        -   Converted `rospy.Publisher` to `node.create_publisher()` with QoS profiles
        -   Converted `rospy.Subscriber` to `node.create_subscription()`
        -   Updated logging: `rospy.loginfo()` → `node.get_logger().info()`
        -   Updated TF transforms to use `tf2_ros` API
        -   Replaced `tf.transformations` with `tf_transformations`
        -   Replaced `rospy.Rate` with `node.create_timer()` for clock node
        -   Updated message publishing to use proper message objects (Bool, String)

---

## Part 14: Neural Wrapper ROS Nodes

**Purpose**: ROS nodes using neural network wrapper

**ROS2 Compatibility**: ✅ Converted to ROS2 compatible (2025-12-19 19:41:23) - Converted from `rospy` to `rclpy` and `rospkg` to `ament_index_python`. All three neural wrapper nodes now inherit from `rclpy.node.Node`, use ROS2 publishers/subscribers/services, and updated service callbacks to ROS2 format.

-   `src/png_navigation/scripts/nrrt_star_neural_wrapper_node.py` (✅ converted to ROS2 - uses rclpy, ament_index_python)
-   `src/png_navigation/scripts/nirrt_star_neural_wrapper_node.py` (✅ converted to ROS2 - uses rclpy, ament_index_python)
-   `src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py` (✅ converted to ROS2 - uses rclpy, ament_index_python)
    -   Uses: Part 2 (config), Part 6 (point_cloud_utils), Part 9 or Part 10 (neural wrapper)
    -   **Changes**:
        -   Replaced `rospy` with `rclpy` and `rclpy.node.Node`
        -   Replaced `rospkg.RosPack()` with `ament_index_python.packages.get_package_share_directory()`
        -   Converted `rospy.Publisher` to `node.create_publisher()` with QoS profiles
        -   Converted `rospy.Subscriber` to `node.create_subscription()`
        -   Converted `rospy.Service` to `node.create_service()` with ROS2 service callback format (request, response)
        -   Updated time handling: `rospy.Time.now()` → `node.get_clock().now().to_msg()`
        -   Updated logging: `rospy.loginfo()` → `node.get_logger().info()`
        -   Updated service request format: `request.request_env` → `request.env` (ROS2 service structure)

---

## Part 15: Dynamic Obstacles Handling

**Purpose**: Scripts for handling dynamic obstacles

**ROS2 Compatibility**: ❌ Needs ROS2 conversion - All files use `rospy` for ROS1 nodes, topics, and services. Need to convert to `rclpy` for ROS2.

-   `src/png_navigation/scripts_dynamic_obstacles/global_planner_node_check.py` (❌ uses rospy, rospkg)
-   `src/png_navigation/scripts_dynamic_obstacles/local_planner_node_check.py` (❌ uses rospy)
-   `src/png_navigation/scripts_dynamic_obstacles/human_checker_gazebo.py` (❌ uses rospy, tf)
-   `src/png_navigation/scripts_dynamic_obstacles/moving_humans_with_noisy_measurements.py` (❌ uses rospy)
    -   Uses: Multiple parts (varies by file)

---

## Part 16: Package Setup

**Purpose**: Package initialization files

**ROS2 Compatibility**: ⚠️ Partially compatible - `setup.py` uses `catkin_pkg` (ROS1 build system). For ROS2, would need `ament_python` setup. `__init__.py` files are ROS-agnostic.

-   `src/png_navigation/setup.py` (⚠️ uses catkin_pkg - ROS1 build system)
-   `src/png_navigation/src/png_navigation/__init__.py` (✅ ROS2 compatible)
-   `src/png_navigation/src/png_navigation/path_planning_classes/__init__.py` (✅ ROS2 compatible)
-   `src/png_navigation/src/png_navigation/maps/__init__.py` (✅ ROS2 compatible)
-   `src/png_navigation/src/png_navigation/datasets/__init__.py` (✅ ROS2 compatible)
-   `src/png_navigation/src/png_navigation/configs/__init__.py` (✅ ROS2 compatible)

---

## Independence Guarantee

✅ **Each part is independent** - no part depends on another part at the same level

✅ **Dependencies are one-way** - if Part A uses Part B, Part B never uses Part A

✅ **Clear separation** - each part has a distinct purpose and can be understood/modified independently

---

## ROS2 Compatibility Summary

**✅ ROS2 Compatible (13 parts):**

-   Part 1: Core Utilities
-   Part 2: Configuration
-   Part 3: Path Planning Utilities Wrapper
-   Part 5: Map Utilities
-   Part 6: Point Cloud Utilities
-   Part 7: Neural Network Base Utilities
-   Part 8: Neural Network Models
-   Part 9: Neural Network Wrapper
-   Part 10: Neural Network Wrapper with BFS
-   Part 12: Global Planner - ✅ Converted (2025-12-19 19:24:55)
-   Part 13: Local Planner - ✅ Converted (2025-12-19 19:36:51)
-   Part 14: Neural Wrapper ROS Nodes - ✅ Converted (2025-12-19 19:41:23)
-   Part 16: Package Setup (**init**.py files only)

**❌ Needs ROS2 Conversion (3 parts):**

-   Part 4: Path Planning Algorithms (4 out of 5 files use rospy)
-   Part 11: ROS Path Planning Service Nodes
-   Part 15: Dynamic Obstacles Handling

**⚠️ Partially Compatible:**

-   Part 16: Package Setup (setup.py uses catkin_pkg, needs ament_python for ROS2)
