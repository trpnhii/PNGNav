#!/opt/conda/envs/pngenv/bin/python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class LocalPlannerClock(Node):
    def __init__(self):
        super().__init__('png_navigation_local_planner_clock')
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.pub = self.create_publisher(String, 'png_navigation/local_planner_clock', qos_profile)
        self.desired_frequency = 20
        self.timer = self.create_timer(1.0 / self.desired_frequency, self.timer_callback)
    
    def timer_callback(self):
        msg = String()
        msg.data = "dummy msg for local planner"
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = LocalPlannerClock()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()