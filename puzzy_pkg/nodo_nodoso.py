#!/usr/bin/env python3
import rclpy, numpy as np, time
from rclpy import qos
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class OdometryNode(Node):
    def __init__(self):
        super().__init__("nodo_nodoso")
        self.get_logger().info("NodoNodoso nodeando...")

        # Timer to compute and publish odometry every 0.1 seconds
        self.create_timer(10.0, self.timer_cb)

        # Subscriptions to encoder velocity topics (Right and Left wheel)
        self.sub = self.create_subscription(Float32, "/VelocityEncR", self.wR_cb, qos.qos_profile_sensor_data)
        self.sub = self.create_subscription(Float32, "/VelocityEncL", self.wL_cb, qos.qos_profile_sensor_data)

        self.pub = self.create_publisher(Twist, "/cmd_vel", 1)

        # Encoder readings
        #self.wR = 0.0  # Angular velocity of the right wheel
        #self.wL = 0.0  # Angular velocity of the left wheel

        self.data_wR = []
        self.data_wL = []

        self.msg_vel = Twist()
        self.msg_vel.linear.x = 0.5
        self.pub.publish(self.msg_vel)
        self.msg_vel.linear.x = 0.0

    
    def wR_cb(self, msg):
        # Callback to update right wheel angular velocity
        if len(self.data_wR)<710:
            self.data_wR.append(msg.data)

    def wL_cb(self, msg):
        # Callback to update left wheel angular velocity
        if len(self.data_wL)<710:
            self.data_wL.append(msg.data)

    def timer_cb(self):
        print("ya pasaron 10 segundos")
        self.pub.publish(self.msg_vel)

        print(len(self.data_wR), "encoder derecho")
        print(len(self.data_wL), "encoder izquierdo")

        W = np.column_stack((self.data_wL,self.data_wR))
        
        self.destroy_node()



def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Node terminated by user.")

if __name__ == "__main__":
    main()