import rclpy
from rclpy import qos
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
# from pynput import keyboard
# import threading
import time
from adafruit_servokit import ServoKit

from src.utilize import *

kit = ServoKit(channels=16)
Grip1 = kit.servo[0]
Grip2 = kit.servo[1]
Grip3 = kit.servo[2]
Grip4 = kit.servo[3]
BallUP_DOWN = kit.servo[4]
BallLeftGrip = kit.servo[5]
BallRightGrip = kit.servo[6]

Grip1.angle = 0
Grip2.angle = 0
Grip3.angle = 0
Grip4.angle = 0
Grip1min: int = 0
Grip1max: int = 180
Grip2min: int = 0
Grip2max: int = 180
Grip3min: int = 0
Grip3max: int = 180
Grip4min: int = 0
Grip4max: int = 180

Auto = False

Grip1minAdjust = 0
Grip1maxAdjust = 180
Grip2minAdjust = 0
Grip2maxAdjust = 180
Grip3minAdjust = 0
Grip3maxAdjust = 180
Grip4minAdjust = 0
Grip4maxAdjust = 180

# BallUP_DOWN.angle   = 180
# BallLeftGrip.angle  = 180
# BallRightGrip.angle = 0


class mainRun(Node):
    
    x :float = 0.0
    y :float = 0.0
    getkey = ''
    Auto = True
    LastTime = time.time()
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
        
        self.create_subscription(
            Twist, 'send_where_mob', self.mobs_callback, 10
        )

        last_mob_msg = Twist()

        self.sent_data_timer = self.create_timer(0.05, self.sendData)

    def on_press(self, key):
        try:
            # self.get_logger().info(f'Key pressed: {key.char}')
            keyboard_msg = String()
            # keyboard_msg.data = f'Key pressed: {key.char}'
            self.getkey = key.char
            keyboard_msg.data = str(self.getkey)
            
            self.send_keyboard.publish(keyboard_msg)
            
        except AttributeError:
            # self.get_logger().info(f'Special key pressed: {key}')
            return

    def on_release(self, key):
        # self.get_logger().info(f'Key released: {key}')
        # if key == keyboard.Key.esc:
        #     self.get_logger().info('Exiting...')
        #     rclpy.shutdown()
        return

    # def start_listening(self):
    #     self.keyboard_callback()
    #     with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
    #         self.get_logger().info('Listening for keyboard input...')
    #         listener.join()

    def keyboard_callback(self, msg = ''):
        # key = msg.data.strip()
        print(f"Received input: {msg}")
        if hasattr(msg, 'data'):
            self.getkey = msg.data.strip()
        else:
            self.getkey = msg.strip()
        print(f"Processed key: {(self.getkey)}")
        # Handle key combinations
        # pyautogui.hotkey(*keys)
            
    def mobs_callback(self, msg):
        if self.Auto == True:
            CurrentTime = time.time()
            section_screen = 810 / 4
            Dt = CurrentTime - self.LastTime
            if Dt < 100:
                if msg.linear.x <= section_screen:
                    Grip1.angle = 170
                    Grip2.angle = 0
                    Grip3.angle = 0
                    Grip4.angle = 0
                elif msg.linear.x <= section_screen * 2:
                    Grip1.angle = 0
                    Grip2.angle = 170
                    Grip3.angle = 0
                    Grip4.angle = 0
                elif msg.linear.x <= section_screen * 3:
                    Grip1.angle = 0
                    Grip2.angle = 0
                    Grip3.angle = 170
                    Grip4.angle = 0
                elif msg.linear.x <= section_screen * 4:
                    Grip1.angle = 0
                    Grip2.angle = 0
                    Grip3.angle = 0
                    Grip4.angle = 170
            elif Dt > 100:
                Grip1.angle = 0
                Grip2.angle = 0
                Grip3.angle = 0
                Grip4.angle = 0
            
            self.last_mob_msg = msg
            self.LastTime = CurrentTime if self.last_mob_msg != msg else self.LastTime
        # print(f"Received mob position: {msg}")
        # Handle mob position
        # BallUP_DOWN.angle   = msg.linear.x
        # BallLeftGrip.angle  = msg.linear.y
        # BallRightGrip.angle = msg.angular.z
    
    def sendData(self): 
        servo_position_msg = String()
        servo_position_msg.data = ""
        
        if self.getkey in ['t', 'g','y', 'h', 'u', 'j', 'i', 'k', 'c']:
            self.Auto = False
            Grip1.angle = Grip1.angle + 2 if self.getkey == 't' else (Grip1.angle - 2 if self.getkey == 'g' else Grip1.angle)
            Grip2.angle = Grip2.angle + 2 if self.getkey == 'y' else (Grip2.angle - 2 if self.getkey == 'h' else Grip2.angle)
            Grip3.angle = Grip3.angle + 2 if self.getkey == 'u' else (Grip3.angle - 2 if self.getkey == 'j' else Grip3.angle)
            Grip4.angle = Grip4.angle + 2 if self.getkey == 'i' else (Grip4.angle - 2 if self.getkey == 'k' else Grip4.angle)
            Grip1.angle = clip(Grip1.angle, Grip1min, Grip1max)
            Grip2.angle = clip(Grip2.angle, Grip2min, Grip2max)
            Grip3.angle = clip(Grip3.angle, Grip3min, Grip3max)
            Grip4.angle = clip(Grip4.angle, Grip4min, Grip4max)
        
        if self.getkey == 'v':
            self.Auto = True
            
        
        self.send_servo_position.publish(servo_position_msg)
        
def main():
    rclpy.init()

    sub = mainRun()   
    # sub_thread = threading.Thread(target=sub.start_listening)
    # sub_thread.start()
    rclpy.spin(sub)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
