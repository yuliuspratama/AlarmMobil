# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV
import numpy as np
import cv2
# import Person
import time
# import firebase
# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV
# import cv2

# capture frames from a video
cap = cv2.VideoCapture(0)

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('cars.xml')


line_up = 9#int(2*(h/6)) #nilai asli int(2*(h/5))
line_down = 99 #int(3*(h/5)) #nilai asli int(3*(h/5))
# POINTS
pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-2,1,2))



# loop runs if capturing has been initialized.
while True:
    # reads frames from a video
    ret, frames = cap.read()

    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)


    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    # To draw a rectangle in each cars
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
   #draw
   cv.Rectangle(frames, 3,7, color, thickness=1, lineType=8, shift=0)
   # Display frames in a window
    cv2.imshow('video2', frames)

    # Wait for Esc key to stop
    if cv2.waitKey(33) == 27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()
