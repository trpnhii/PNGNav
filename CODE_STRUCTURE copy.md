# PNG Navigation Code Structure - Independent Parts

**Organization**: Files are grouped into parts where:

-   **No two parts have ANY dependencies between them** (not even one-way)
-   **No shared files** - each file appears in exactly one part
-   Files within the same part can depend on each other
-   Each part is completely independent and self-contained

---

## Part 1: Main Navigation System

**Purpose**: Complete navigation system including path planning, map processing, neural guidance, global planner, and dynamic obstacles handling

**Files**:

-   `src/png_navigation/src/png_navigation/path_planning_classes/collision_check_utils.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_env_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_visualizer_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_utils_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_base_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/rrt_star_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/irrt_star_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/nrrt_star_png_2d.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/nirrt_star_png_2d.py`
-   `src/png_navigation/src/png_navigation/configs/rrt_star_config.py`
-   `src/png_navigation/src/png_navigation/maps/map_utils.py`
-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/models/pointnet2_utils.py`
-   `src/png_navigation/src/png_navigation/wrapper/utils/bfs_connect_heuristic.py`
-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/models/pointnet2_sem_seg_msg_pathplan.py`
-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/pointnet2_wrapper.py`
-   `src/png_navigation/src/png_navigation/wrapper/pointnet_pointnet2/pointnet2_wrapper_connect_bfs.py`
-   `src/png_navigation/src/png_navigation/datasets/point_cloud_mask_utils_updated.py`
-   `src/png_navigation/scripts/rrt_star_node.py`
-   `src/png_navigation/scripts/irrt_star_node.py`
-   `src/png_navigation/scripts/nrrt_star_node.py`
-   `src/png_navigation/scripts/nirrt_star_node.py`
-   `src/png_navigation/scripts/global_planner_node.py`
-   `src/png_navigation/scripts/nrrt_star_neural_wrapper_node.py`
-   `src/png_navigation/scripts/nirrt_star_neural_wrapper_node.py`
-   `src/png_navigation/scripts/nirrt_star_c_neural_wrapper_node.py`
-   `src/png_navigation/scripts_dynamic_obstacles/global_planner_node_check.py`
-   `src/png_navigation/scripts_dynamic_obstacles/local_planner_node_check.py`
-   `src/png_navigation/scripts_dynamic_obstacles/human_checker_gazebo.py`
-   `src/png_navigation/scripts_dynamic_obstacles/moving_humans_with_noisy_measurements.py`

---

## Part 2: Local Robot Control

**Purpose**: Low-level robot control for waypoint following (completely standalone, no dependencies on Part 1)

**Files**:

-   `src/png_navigation/scripts/local_planner_node.py`
-   `src/png_navigation/scripts/local_planner_clock.py`

---

## Part 3: Package Initialization

**Purpose**: Package setup and initialization files (standalone)

**Files**:

-   `src/png_navigation/setup.py`
-   `src/png_navigation/src/png_navigation/__init__.py`
-   `src/png_navigation/src/png_navigation/path_planning_classes/__init__.py`
-   `src/png_navigation/src/png_navigation/maps/__init__.py`
-   `src/png_navigation/src/png_navigation/datasets/__init__.py`
-   `src/png_navigation/src/png_navigation/configs/__init__.py`

---

## Independence Guarantee

✅ **No dependencies between parts** - Part 1, Part 2, and Part 3 are completely independent

✅ **No shared files** - Each file appears in exactly one part

✅ **True independence** - Parts can be understood, modified, or removed independently without affecting other parts

**Summary**: The codebase is organized into **3 independent parts**:

1. **Part 1**: All interconnected navigation code (path planning, neural networks, maps, ROS nodes)
2. **Part 2**: Standalone local planner
3. **Part 3**: Package setup files
