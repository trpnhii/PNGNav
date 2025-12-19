#!/usr/bin/python3.8
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
import numpy as np
import tf2_ros
from tf2_ros import TransformException
import tf_transformations

from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist, Point, PoseStamped


def normalize_angle(angle):
    normalized_angle = math.fmod(angle + math.pi, 2 * math.pi)
    if normalized_angle < 0:
        normalized_angle += 2*math.pi
    return normalized_angle - math.pi

class LocalPlanner(Node):
    def __init__(
        self,
        robot_frame='base_footprint',
        linear_speed_levels=(0.05, 0.1, 0.2),
        angular_speed_levels=(0.2, 0.4),
        distance_threshold=(0.05, 0.3),
        angle_threshold=(0.05, 0.1),
        linear_speed_increment=0.01,
        angular_speed_increment=0.1,
    ):
        super().__init__('png_navigation_local_planner')
        
        # Setup QoS profile
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        
        self.cmd_vel = self.create_publisher(Twist, 'cmd_vel', qos_profile) # gazebo
        # * self.cmd_vel = self.create_publisher(Twist, 'cmd_vel_mux/input/teleop', qos_profile) # real world
        self.waypoint_reached_pub = self.create_publisher(Bool, '/waypoint_reached', qos_profile)

        # Setup TF2
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.odom_frame = 'map'
        self.base_frame = robot_frame

        self.goal_x = 0.0
        self.goal_y = 0.0
        self.goal_yaw = 0.0
        self.is_global_goal = False

        self.linear_speed_levels = linear_speed_levels
        self.angular_speed_levels = angular_speed_levels
       
        self.linear_speed_increment = linear_speed_increment # 0.01#0.005
        self.angular_speed_increment = angular_speed_increment # 0.1
        self.linear_speed = 0
        self.angular_speed = 0

        self.target_linear_speed = 0
        self.target_angular_speed = 0

        self.distance_threshold = distance_threshold
        self.angle_threshold = angle_threshold
        self.drive_robot = False

        self.create_subscription(PoseStamped, '/waypoint', self.waypoint_callback, qos_profile)
        self.create_subscription(String, 'png_navigation/local_planner_clock', self.clock_callback, qos_profile)
        self.get_logger().info("Local Planner is initialized.")

    def waypoint_callback(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        if msg.pose.position.z != 0:
            self.is_global_goal = True
            angles = tf_transformations.euler_from_quaternion([msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w])
            self.goal_yaw = angles[-1]
        self.drive_robot = True
    
    def clock_callback(self, msg):  # noqa: ARG002
        if not self.drive_robot:
            return
        pose_result = self.get_pose()
        if pose_result is None:
            return
        position, rotation = pose_result
        distance = np.sqrt((self.goal_x - position.x)**2 + (self.goal_y - position.y)**2)
     
        if distance < self.distance_threshold[0]:
            if not self.is_global_goal:
                self.get_logger().info("Waypoint reached.")
                waypoint_reached_msg = Bool()
                waypoint_reached_msg.data = True
                self.waypoint_reached_pub.publish(waypoint_reached_msg)
                return
            else:
                self.target_linear_speed = 0
                remaining_rotation = normalize_angle(self.goal_yaw - rotation)
                if abs(remaining_rotation) > self.angle_threshold[1]:
                    if remaining_rotation > 0:
                        self.target_angular_speed = self.angular_speed_levels[1] # 0.4
                    else:
                        self.target_angular_speed = -self.angular_speed_levels[1] # -0.4
                    self.send_velocity_command(self.target_linear_speed, self.target_angular_speed)
                    return
                elif abs(remaining_rotation) > self.angle_threshold[0]:
                    if remaining_rotation > 0:
                        self.target_angular_speed = self.angular_speed_levels[0] # 0.2
                    else:
                        self.target_angular_speed = -self.angular_speed_levels[0] # -0.2
                    self.send_velocity_command(self.target_linear_speed, self.target_angular_speed)
                    return
                else:
                    self.target_angular_speed = 0
                    self.send_velocity_command(self.target_linear_speed, self.target_angular_speed)
                    if self.linear_speed==0 and self.angular_speed==0:
                        self.get_logger().info("Global goal reached announced by local planner.") # global goal reached
                        waypoint_reached_msg = Bool()
                        waypoint_reached_msg.data = True
                        self.waypoint_reached_pub.publish(waypoint_reached_msg)
                        self.drive_robot = False
                        self.goal_yaw = None
                        self.is_global_goal = False
                        return
        
        path_angle = np.arctan2(self.goal_y - position.y, self.goal_x - position.x)
        remaining_rotation = normalize_angle(path_angle - rotation)
        if abs(remaining_rotation) > self.angle_threshold[1]:
            self.target_linear_speed = 0.
            if remaining_rotation > 0:
                self.target_angular_speed = self.angular_speed_levels[1] # 0.4
            else:
                self.target_angular_speed = -self.angular_speed_levels[1] # -0.4
            self.send_velocity_command(self.target_linear_speed, self.target_angular_speed)
            return
        elif abs(remaining_rotation) > self.angle_threshold[0]:
            if remaining_rotation > 0:
                self.target_angular_speed = self.angular_speed_levels[0] # 0.2
            else:
                self.target_angular_speed = -self.angular_speed_levels[0] # -0.2

            if distance < self.distance_threshold[1] and self.is_global_goal:
                self.target_linear_speed = self.linear_speed_levels[0] # 0.05
            else:
                self.target_linear_speed = self.linear_speed_levels[2] # 0.2
            self.send_velocity_command(self.target_linear_speed, self.target_angular_speed)
            return
        else:
            self.target_angular_speed = 0.
            if distance < self.distance_threshold[1] and self.is_global_goal:
                self.target_linear_speed = self.linear_speed_levels[1] # 0.1
            else:
                self.target_linear_speed = self.linear_speed_levels[2] # 0.2
            self.send_velocity_command(self.target_linear_speed, self.target_angular_speed)
            return
            
    def send_velocity_command(self, target_linear_speed, target_angular_speed):
        if abs(target_linear_speed-self.linear_speed) < self.linear_speed_increment:
            self.linear_speed = target_linear_speed
        else:
            self.linear_speed += self.linear_speed_increment*(target_linear_speed-self.linear_speed)/abs(self.target_linear_speed-self.linear_speed)
        if abs(target_angular_speed-self.angular_speed) < self.angular_speed_increment:
            self.angular_speed = target_angular_speed
        else:
            self.angular_speed += self.angular_speed_increment*(target_angular_speed-self.angular_speed)/abs(self.target_angular_speed-self.angular_speed)
        move_cmd = Twist()
        move_cmd.linear.x = self.linear_speed
        move_cmd.angular.z = self.angular_speed
        self.cmd_vel.publish(move_cmd)

    def get_pose(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.odom_frame, 
                self.base_frame, 
                rclpy.time.Time()
            )
            trans = transform.transform.translation
            rot = transform.transform.rotation
            rotation = tf_transformations.euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])
        except TransformException:
            self.get_logger().info("TF Exception")
            return None
        return Point(x=trans.x, y=trans.y, z=trans.z), rotation[2]

    def shutdown(self):
        self.cmd_vel.publish(Twist())
        time.sleep(1)


if __name__ == '__main__':
    try:
        rclpy.init()
        gp = LocalPlanner()
        rclpy.spin(gp)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            gp.shutdown()
            rclpy.shutdown()


