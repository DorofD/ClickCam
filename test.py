import pyautogui
import cv2
import numpy as np
import random
import threading

recorder_up = True


def recorder():
    global recorder_up
    resolution = tuple(pyautogui.size())
    fps = 12.0
    codec = cv2.VideoWriter_fourcc(*"MJPG")
    filename = "screen_recording"+str(random.randint(0, 1000))+".avi"

    # Creating a VideoWriter object
    writer = cv2.VideoWriter(str(filename), codec, fps, resolution)

    # Creating an Empty window
    # cv2.namedWindow("Screen Recorder", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Screen Recorder", 480, 270)

    while True:
        img = pyautogui.screenshot()
        # Convert the screenshot to a numpy array
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR to RGB

        # Writing it to the output file
        writer.write(frame)

        # Displaying the recording screen
        # cv2.imshow('Screen Recorder', frame)

        # Stop recording when we press 'q'
        # if cv2.waitKey(1) == ord('q'):
        #     print("Recording Stopped")
        #     break
        if recorder_up == False:
            break
    print("Recordings saved as: "+filename)
    writer.release()
    cv2.destroyAllWindows()


t1 = threading.Thread(target=recorder)

t1.start()

a = 0
while True:

    print(a)
    if a == 5:
        break
    if a == 4:
        recorder_up = False
        print(recorder_up)
    a = int(input('Enter 4 for stop recording: '))
