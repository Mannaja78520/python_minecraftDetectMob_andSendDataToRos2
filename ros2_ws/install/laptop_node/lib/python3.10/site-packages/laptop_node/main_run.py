import rclpy
from rclpy import qos
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import pyautogui
from ultralytics import YOLO
import cv2 as cv
import os
from pynput import keyboard
import threading

from laptop_node.windowcapture import WindowCapture
    
model = YOLO('/home/mannaja/coding/project/python_minecraftDetectMob_andSendDataToRos2/ros2_ws/src/laptop_node/laptop_node/best.pt')  # Use your custom model if you have one

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WindowCapture.list_window_names()

# Initialize WindowCapture with a partial window name
partial_name = 'Minecraft* 1.20.4'
wincap = WindowCapture(partial_name, id_type='name')


class mainRun(Node):
    x :float = 0.0
    y :float = 0.0
    def __init__(self):
        super().__init__("Laptop_Node")

        self.sent_where_mob = self.create_publisher(
            Twist, "send_where_mob", qos_profile=qos.qos_profile_system_default
        )
        
        self.send_keyboard = self.create_publisher(
            String, '/laptop/keyboard', 10
        )
        
        self.create_subscription(
            String, '/pi/keyboard', self.keyboard_callback, 10
        )
        
        # self.create_subscription(
        #     String, 'servo_position', self.servo_callback, 10
        # )
        
        self.sent_data_timer = self.create_timer(0.05, self.sendData)

    def on_press(self, key):
        try:
            self.get_logger().info(f'Key pressed: {key.char}')
            keyboard_msg = String()
            keyboard_msg.data = f'Key pressed: {key.char}'
            self.send_keyboard.publish(keyboard_msg)
        except AttributeError:
            self.get_logger().info(f'Special key pressed: {key}')

    def on_release(self, key):
        self.get_logger().info(f'Key released: {key}')
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
        
        # Handle key combinations
        pyautogui.hotkey(*keys)
            
    def detectMobs(self):
        screenshot = wincap.get_screenshot()

        results = model.predict(screenshot)
        # Check if there are any detections
        if len(results[0].boxes) > 0:
            self.x = results[0].boxes.xywh[0][0].item()
            self.y = results[0].boxes.xywh[0][1].item()
            # print(self.x)
            # print(self.y)
        else:
            print("No detections")

        # Plot the results
        plot_img = results[0].plot()

        # Resize the image to one-quarter size
        height, width = plot_img.shape[:2]
        # resized_img = cv.resize(plot_img, (width // 4, height // 4))

        # Draw lines to divide the image into four equal parts along the x-axis
        part_width = width // 4
        cv.line(plot_img, (part_width, 0), (part_width, height), (0, 255, 0), 2)
        cv.line(plot_img, (2 * part_width, 0), (2 * part_width, height), (0, 255, 0), 2)
        cv.line(plot_img, (3 * part_width, 0), (3 * part_width, height), (0, 255, 0), 2)


        cv.imshow('Combined Images', plot_img)
        cv.waitKey(1)
        
    def sendData(self): 
        mobdata_msg = Twist()
        
        self.detectMobs()
        
        mobdata_msg.linear.x = self.x
        mobdata_msg.linear.y = self.y
        
        self.sent_where_mob.publish(mobdata_msg)
        
def main():
    rclpy.init()

    sub = mainRun()   
    sub_thread = threading.Thread(target=sub.start_listening)
    sub_thread.start()
    rclpy.spin(sub)
    rclpy.shutdown()
    cv.destroyAllWindows()
    
    
if __name__ == "__main__":
    main()
