from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value='map_gazebo',
            description='Map name to use'
        ),
        Node(
            package='png_navigation',
            executable='irrt_star_node.py',
            name='irrt_star_node',
            output='screen',
        ),
        Node(
            package='png_navigation',
            executable='local_planner_clock.py',
            name='local_planner_clock',
            output='screen',
        ),
        Node(
            package='png_navigation',
            executable='local_planner_node.py',
            name='local_planner_node',
            output='screen',
        ),
        Node(
            package='png_navigation',
            executable='global_planner_node.py',
            name='global_planner_node',
            output='screen',
            arguments=['--map', LaunchConfiguration('map')],
        ),
    ])
