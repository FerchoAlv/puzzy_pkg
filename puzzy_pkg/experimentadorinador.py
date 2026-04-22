#!/usr/bin/env python3
import rclpy, numpy as np, time, csv
from rclpy import qos
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from pathlib import Path

class NodingNode(Node):
    def __init__(self):
        super().__init__("experimentadorinador")
        self.get_logger().info("expermentando los experimentos experimentosos")

        # Timer to compute and publish odometry every 0.1 seconds
        self.create_timer(0.1, self.st_machine)

        # Subscriptions to encoder velocity topics (Right and Left wheel)
        self.sub = self.create_subscription(Float32, "/VelocityEncR", self.wR_cb, qos.qos_profile_sensor_data)
        self.sub = self.create_subscription(Float32, "/VelocityEncL", self.wL_cb, qos.qos_profile_sensor_data)

        self.pub = self.create_publisher(Twist, "/cmd_vel", 1)


        # carpeta del archivo actual
        self.exp_num = 1
        self.velocidades = [0.2, 0.5, 0.7, 0.9, 1.0]
        self.selected_vel = 0 # velocidad actual, va desde 0 hasta len(velocidades)-1

        dir_salida = Path.home() / "ros2_ws" / "src" / "puzzy_pkg" / f"data_{self.velocidades[self.selected_vel]}"
        dir_salida.mkdir(parents=True, exist_ok=True)
        self.ruta_salida = dir_salida / f"datos_{self.exp_num}.csv"

        self.data_wR = []
        self.data_wL = []

        self.t0 = 0.0       

        self.state = "inicio"
        self.next_state = False

        self.msg_vel = Twist()
        self.msg_vel.linear.x = 0.0

    
    def wR_cb(self, msg):
        # Callback to update right wheel angular velocity
        if self.state == "experimentanding":
            if len(self.data_wR)<710:
                self.data_wR.append(msg.data)

    def wL_cb(self, msg):
        # Callback to update left wheel angular velocity
        if self.state == "experimentanding":
            if len(self.data_wL)<710:
                self.data_wL.append(msg.data)


    def update_exit_dir(self):
        dir_salida = Path.home() / "ros2_ws" / "src" / "puzzy_pkg" / f"data_{self.velocidades[self.selected_vel]}"
        dir_salida.mkdir(parents=True, exist_ok=True)
        self.ruta_salida = dir_salida / f"datos_{self.exp_num}.csv"



    def st_machine(self):
        print(self.state)

        #Transitions"
        if self.state == "inicio" and self.next_state == True:  #iniciando el experimentador inador
            self.state = "experimentanding"
            self.next_state = False
            self.t0 = time.time()

        elif self.state == "experimentanding" and self.next_state == True: #que sepa el mundo que en marcha estoy que disfruto cada instante aquiiiiiiiiiiiiiii
            self.state = "calculanding"
            self.next_state = False

        elif self.state == "calculanding" and self.next_state == True:
            if self.exp_num <= 5:
                self.state = "inicio"
                self.next_state = False
            else:
                self.state = "acabo"
                self.next_state = False
            

        #Actions-States
        if self.state == "inicio": #inicia bun nuevo experimento 
            self.data_wR.clear()
            self.data_wL.clear()
            self.next_state = True    


        if self.state == "experimentanding": #inicia a recopilar datos del experimento
            self.msg_vel.linear.x = 0.5
            self.pub.publish(self.msg_vel)

            elapsed_t = time.time() - self.t0
            print(f"Tiempo en experimento: {elapsed_t:.2f} s")
            #recompilando datos muy datosos y asi
            if elapsed_t >= 10:
                print("ya pasaron 10 segundos")
                self.msg_vel.linear.x = 0.0
                self.pub.publish(self.msg_vel)
                self.next_state = True


        if self.state == "calculanding":
            print("calculando calculos muy calculosos. . .")
            print("ya acabe de calcular")

            print(len(self.data_wR), "encoder derecho")
            print(len(self.data_wL), "encoder izquierdo") 

            W = np.column_stack((self.data_wL,self.data_wR))
            with open(self.ruta_salida, "w", newline="", encoding="utf-8") as f: 
                writer = csv.writer(f)
                writer.writerows(W)

            self.exp_num += 1
            self.update_exit_dir()
            time.sleep(4)
            self.next_state = True


        if self.state == "acabo":
            print("Y A     S E     A C A B O     T O D O ")
            self.destroy_node()
            



def main(args=None):
    rclpy.init(args=args)
    node = NodingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Node terminated by user.")

if __name__ == "__main__":
    main()




