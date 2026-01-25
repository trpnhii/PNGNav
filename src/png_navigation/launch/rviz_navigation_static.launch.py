from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    rviz_config_path = os.path.join(
        get_package_share_directory('png_navigation'),
        'rviz',
        'navigation_static.rviz'
    )
    
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            arguments=['-d', rviz_config_path],
            output='screen',
        ),
    ])
