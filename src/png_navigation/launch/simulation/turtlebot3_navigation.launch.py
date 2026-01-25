"""
TurtleBot3 Navigation Launch File for Gazebo Simulation
Launches map_server and AMCL for localization.
Robot state publisher is already running from Gazebo.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.actions import Node, LifecycleNode
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Get package paths
    png_nav_share = get_package_share_directory('png_navigation')
    nav2_bringup_share = get_package_share_directory('nav2_bringup')
    
    # Default map file
    default_map = os.path.join(png_nav_share, 'maps', 'map_gazebo.yaml')
    
    # Arguments
    map_file_arg = DeclareLaunchArgument(
        'map',
        default_value=default_map,
        description='Path to map yaml file'
    )
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock'
    )
    
    # Map server node
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': LaunchConfiguration('map'),
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )
    
    # Lifecycle manager to activate map_server
    lifecycle_manager_map = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map_server',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': ['map_server']
        }]
    )
    
    # AMCL node for localization
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_model_type': 'nav2_amcl::DifferentialMotionModel',
            'base_frame_id': 'base_footprint',
            'odom_frame_id': 'odom',
            'global_frame_id': 'map',
            'scan_topic': '/scan',
            'initial_pose': {
                'x': -2.0,
                'y': -0.5,
                'z': 0.0,
                'yaw': 0.0
            }
        }]
    )
    
    # Lifecycle manager for AMCL
    lifecycle_manager_amcl = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_amcl',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': ['amcl']
        }]
    )
    
    return LaunchDescription([
        map_file_arg,
        use_sim_time_arg,
        map_server,
        lifecycle_manager_map,
        amcl,
        lifecycle_manager_amcl,
    ])
