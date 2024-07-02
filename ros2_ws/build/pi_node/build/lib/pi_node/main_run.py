import rclpy
from rclpy import qos
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from pynput import keyboard
import threading
# from adafruit_servokit import ServoKit

# from src.utilize import *

# kit = ServoKit(channels=16)
# Grip1 = kit.servo[0]
# Grip2 = kit.servo[1]
# Grip3 = kit.servo[2]
# Grip4 = kit.servo[3]
# BallUP_DOWN = kit.servo[4]
# BallLeftGrip = kit.servo[5]
# BallRightGrip = kit.servo[6]

# Grip1.angle = 0
# Grip2.angle = 0
# Grip3.angle = 0
# Grip4.angle = 0
# BallUP_DOWN.angle   = 180
# BallLeftGrip.angle  = 180
# BallRightGrip.angle = 0


class mainRun(Node):
    x :float = 0.0
    y :float = 0.0
    def __init__(self):
        super().__init__("Pi_Node")

        self.send_servo_position = self.create_publisher(
            String, 'servo_position', 100
        )
        
        self.send_keyboard = self.create_publisher(
            String, '/pi/keyboard', 10
        )
        
        self.create_subscription(
            Twist, '/laptop/keyboard', self.keyboard_callback, 10
        )

        self.sent_data_timer = self.create_timer(0.05, self.sendData)

    def on_press(self, key):
        try:
            # self.get_logger().info(f'Key pressed: {key.char}')
            keyboard_msg = String()
            keyboard_msg.data = f'Key pressed: {key.char}'
            self.send_keyboard.publish(keyboard_msg)
            
            
            
            
        except AttributeError:
            # self.get_logger().info(f'Special key pressed: {key}')
            return

    def on_release(self, key):
        # self.get_logger().info(f'Key released: {key}')
        if key == keyboard.Key.esc:
            self.get_logger().info('Exiting...')
            rclpy.shutdown()

    def start_listening(self):
        self.keyboard_callback()
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.get_logger().info('Listening for keyboard input...')
            listener.join()

    def keyboard_callback(self, msg = ''):
        keys = msg.split('+')
        self.get_logger().info(f'Received keys: {keys}')
        print(keys)
        # Handle key combinations
        # pyautogui.hotkey(*keys)
            
    def sendData(self): 
        servo_position_msg = String()
        servo_position_msg.data = ""
        
        
        self.send_servo_position.publish(servo_position_msg)
        
def main():
    rclpy.init()

    sub = mainRun()   
    sub_thread = threading.Thread(target=sub.start_listening)
    sub_thread.start()
    rclpy.spin(sub)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
