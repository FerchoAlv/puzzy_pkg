#!/usr/bin/env python3
import rclpy, numpy as np, random
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class OdometryNode(Node):
    def __init__(self):
        super().__init__("prueboso")
        self.get_logger().info("prueboso pruebeando...")

        # Timer to compute and publish odometry every 0.1 seconds
        self.create_timer(0.01, self.timer_cb)

        # Subscriptions to encoder velocity topics (Right and Left wheel)
        self.pubR = self.create_publisher(Float32, "/VelocityEncR", 1)
        self.pubL = self.create_publisher(Float32, "/VelocityEncL", 1)
        self.sub = self.create_subscription(Twist, "/cmd_vel", self.cmd_cb,1)
        self.msg_enc = Float32()
        self.publicamos = False

    def cmd_cb(self, msg):
        dato = msg.linear.x
        if dato != 0.0:
            self.publicamos = True
        elif dato == 0.0:
            self.publicamos = False
        


    def timer_cb(self):
        if self.publicamos:
            self.msg_enc.data = random.uniform(0, 5)
            self.pubR.publish(self.msg_enc)
            self.msg_enc.data = random.uniform(0, 5)
            self.pubL.publish(self.msg_enc)




def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Node terminated by user.")

if __name__ == "__main__":
    main()