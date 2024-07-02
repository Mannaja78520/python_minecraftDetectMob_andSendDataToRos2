import cv2 as cv
import os
from src.windowcapture import WindowCapture
from ultralytics import YOLO

class mobDetector:
    x :float = 0.0
    y :float = 0.0
    
    def __init__(self):
        self.model = YOLO('best.pt')  # Use your custom model if you have one

        # Change the working directory to the folder this script is in.
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # List all open window names to get the correct identifier
        WindowCapture.list_window_names()

        # Initialize WindowCapture with a partial window name
        partial_name = 'Minecraft* 1.20.4'
        self.wincap = WindowCapture(partial_name, id_type='name')

    
    def detectMobs(self):
        # get an updated image of the window
        screenshot = self.wincap.get_screenshot()

        results = self.model.predict(screenshot)
        
        # Check if there are any detections
        if len(results[0].boxes) > 0:
            self.x = results[0].boxes.xywh[0][0].item()
            self.y = results[0].boxes.xywh[0][1].item()
            # print(x)
            # print(y)
        else:
            print("No detections")

        # Plot the results
        plot_img = results[0].plot()

        # Resize the image to one-quarter size
        height, width = plot_img.shape[:2]

        # Draw lines to divide the image into four equal parts along the x-axis
        part_width = width // 4
        cv.line(plot_img, (part_width, 0), (part_width, height), (0, 255, 0), 2)
        cv.line(plot_img, (2 * part_width, 0), (2 * part_width, height), (0, 255, 0), 2)
        cv.line(plot_img, (3 * part_width, 0), (3 * part_width, height), (0, 255, 0), 2)


        cv.imshow('Combined Images', plot_img)