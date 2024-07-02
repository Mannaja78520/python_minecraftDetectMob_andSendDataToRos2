import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from ultralytics import YOLO

model = YOLO('runs/detect/train5/weights/best.pt')  # Use your custom model if you have one

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# List all open window names to get the correct identifier
WindowCapture.list_window_names()

# Initialize WindowCapture with a partial window name
partial_name = 'Minecraft* 1.20.4'
wincap = WindowCapture(partial_name, id_type='name')

loop_time = time()
while True:
    # get an updated image of the window
    screenshot = wincap.get_screenshot()

    results = model.predict(screenshot)
    # print(results)

    # display the screenshot
    # results[0].save()

    # Check if there are any detections
    if len(results[0].boxes) > 0:
        x: float = results[0].boxes.xywh[0][0].item()
        y: float = results[0].boxes.xywh[0][1].item()
        print(x)
        print(y)
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
    
    # sleep(0.1)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')