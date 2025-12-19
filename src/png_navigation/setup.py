## ROS2 setup.py - Use ament_python for ROS2

from setuptools import setup
from glob import glob
import os

package_name = 'png_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files if any
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'launch_dynamic_obstacles'), glob('launch_dynamic_obstacles/*.launch.py')),
        # Include rviz configs if any
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zhe',
    maintainer_email='zhe@todo.todo',
    description='The png_navigation package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Add entry points for executable scripts if needed
        ],
    },
)