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

-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_utils_2d.py`
    -   Uses: Part 1 (collision_check_utils)

---

## Part 4: Path Planning Algorithms

**Purpose**: All RRT algorithm implementations

-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_base_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_star_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/irrt_star_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/nrrt_star_png_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/nirrt_star_png_2d.py`
    -   Uses: Part 1 (rrt_utils_2d, rrt_visualizer_2d), Part 3 (rrt_utils_2d)

---

## Part 5: Map Utilities

**Purpose**: Map processing and coordinate transformation

-   `src/png_navigation/src/png_navigation/maps/map_utils.py`
    -   Uses: Part 1 (collision_check_utils)

---

## Part 6: Point Cloud Utilities

**Purpose**: Point cloud generation and processing

-   `src/png_navigation/src/png_navigation/datasets/point_cloud_mask_utils_updated.py`
    -   Uses: Part 1 (collision_check_utils)

---

## Part 7: Neural Network Base Utilities

**Purpose**: Base neural network utilities (standalone)

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/models/pointnet2_utils.py`
-   `src/png_navigation/src/png_navigation/wrapper/utils/bfs_connect_heuristic.py`

---

## Part 8: Neural Network Models

**Purpose**: Neural network model definitions

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/models/pointnet2_sem_seg_msg_pathplan.py`
    -   Uses: Part 7 (pointnet2_utils)

---

## Part 9: Neural Network Wrapper

**Purpose**: Main neural network wrapper class

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/pointnet2_wrapper.py`
    -   Uses: Part 7 (pointnet2_utils), Part 8 (models)

---

## Part 10: Neural Network Wrapper with BFS

**Purpose**: Neural network wrapper with BFS connection heuristic

-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/pointnet2_wrapper_connect_bfs.py`
    -   Uses: Part 6 (point_cloud_mask_utils), Part 7 (pointnet2_utils, bfs_connect_heuristic), Part 8 (models)

---

## Part 11: ROS Path Planning Service Nodes

**Purpose**: ROS service nodes for path planning algorithms

-   `src/png_navigation/scripts/rrt_star_node.py`
-   `src/png_navigation/scripts/irrt_star_node.py`
-   `src/png_navigation/scripts/nrrt_star_node.py`
-   `src/png_navigation/scripts/nirrt_star_node.py`
    -   Uses: Part 1 (rrt_env_2d), Part 2 (config), Part 4 (algorithms)

---

## Part 12: Global Planner

**Purpose**: High-level navigation planner

-   `src/png_navigation/scripts/global_planner_node.py`
    -   Uses: Part 1 (rrt_env_2d), Part 2 (config), Part 5 (map_utils)

---

## Part 13: Local Planner

**Purpose**: Low-level robot control (standalone ROS node)

-   `src/png_navigation/scripts/local_planner_node.py`
-   `src/png_navigation/scripts/local_planner_clock.py`

---

## Part 14: Neural Wrapper ROS Nodes

**Purpose**: ROS nodes using neural network wrapper

-   `src/png_navigation/scripts/nrrt_star_neural_wrapper_node.py`
-   `src/png_navigation/scripts/nirrt_star_neural_wrapper_node.py`
-   `src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py`
    -   Uses: Part 2 (config), Part 6 (point_cloud_utils), Part 9 or Part 10 (neural wrapper)

---

## Part 15: Dynamic Obstacles Handling

**Purpose**: Scripts for handling dynamic obstacles

-   `src/png_navigation/scripts_dynamic_obstacles/global_planner_node_check.py`
-   `src/png_navigation/scripts_dynamic_obstacles/local_planner_node_check.py`
-   `src/png_navigation/scripts_dynamic_obstacles/human_checker_gazebo.py`
-   `src/png_navigation/scripts_dynamic_obstacles/moving_humans_with_noisy_measurements.py`
    -   Uses: Multiple parts (varies by file)

---

## Part 16: Package Setup

**Purpose**: Package initialization files

-   `src/png_navigation/setup.py`
-   `src/png_navigation/src/png_navigation/__init__.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/__init__.py`
-   `src/png_navigation/src/png_navigation/maps/__init__.py`
-   `src/png_navigation/src/png_navigation/datasets/__init__.py`
-   `src/png_navigation/src/png_navigation/configs/__init__.py`

---

## Independence Guarantee

✅ **Each part is independent** - no part depends on another part at the same level

✅ **Dependencies are one-way** - if Part A uses Part B, Part B never uses Part A

✅ **Clear separation** - each part has a distinct purpose and can be understood/modified independently
