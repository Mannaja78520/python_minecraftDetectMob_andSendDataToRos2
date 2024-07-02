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
    cv.imshow('Computer Vision', screenshot)
    results[0].show()
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