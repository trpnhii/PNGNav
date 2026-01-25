#!/opt/conda/envs/pngenv/bin/python
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
import numpy as np

from geometry_msgs.msg import Pose, PoseArray


class PoseArrayPublisher(Node):
    def __init__(self):
        super().__init__('pose_array_publisher')
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.pose_array_pub = self.create_publisher(PoseArray, 'dr_spaam_detections', qos_profile)
        self.real_pose_array_pub = self.create_publisher(PoseArray, 'gt_human_positions', qos_profile)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.px, self.py = 1, -0.8
        self.count_turn = 40
        self.vx, self.vy = -1/20., 0
        self.count = 0
        self.ts = time.time()

    def timer_callback(self):
        pose_array_msg = PoseArray()
        real_pose_array_msg = PoseArray()
        if self.count > self.count_turn:
            self.vx = -self.vx
            self.count = 0
        self.px += self.vx
        self.py += self.vy
        self.count += 1

        for i in range(1):
            pose = Pose()
            pose.position.x = self.px+np.random.randn()*0.01
            pose.position.y = self.py+np.random.randn()*0.01
            pose.position.z = 0.0
            pose.orientation.x = 0.0
            pose.orientation.y = 0.0
            pose.orientation.z = 0.0
            pose.orientation.w = 1.0
            pose_array_msg.poses.append(pose)

        if time.time() - self.ts > 2:
            pose = Pose()
            pose.position.x = -1.5+np.random.randn()*0.01
            pose.position.y = 0.5+np.random.randn()*0.01
            pose.position.z = 0.0
            pose.orientation.x = 0.0
            pose.orientation.y = 0.0
            pose.orientation.z = 0.0
            pose.orientation.w = 1.0
            pose_array_msg.poses.append(pose)   

        pose_array_msg.header.stamp = self.get_clock().now().to_msg()
        pose_array_msg.header.frame_id = "map"
        pose = Pose()
        pose.position.x = self.px
        pose.position.y = self.py
        pose.position.z = 0.0
        pose.orientation.x = 0.0
        pose.orientation.y = 0.0
        pose.orientation.z = 0.0
        pose.orientation.w = 1.0
        real_pose_array_msg.poses.append(pose)

        if time.time() - self.ts > 2:
            pose = Pose()
            pose.position.x = -1.5
            pose.position.y = 0.5
            pose.position.z = 0.0
            pose.orientation.x = 0.0
            pose.orientation.y = 0.0
            pose.orientation.z = 0.0
            pose.orientation.w = 1.0
            real_pose_array_msg.poses.append(pose)   
        real_pose_array_msg.header.stamp = self.get_clock().now().to_msg()
        real_pose_array_msg.header.frame_id = "map"
        self.pose_array_pub.publish(pose_array_msg)
        self.real_pose_array_pub.publish(real_pose_array_msg)


def main():
    rclpy.init()
    node = PoseArrayPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()