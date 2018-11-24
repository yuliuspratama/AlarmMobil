# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV
import numpy as np
import cv2
# import Person
import time
# import firebase
import serial

#Contadores de entrada y salida
cnt_up   = 0
cnt_down = 0

cnt_lift   = 0
cnt_right = 0

# capture frames from a video
cap = cv2.VideoCapture("VID_20181029_095024.mp4")

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('Test.xml')

#Cetak properti pengambilan ke konsol
for i in range(19): #range asli 19
    print i, cap.get(i)

w = cap.get(3) #nilai asli 3
h = cap.get(4) #nilai asli 4
frameArea = 2*(h*w) #nilai asli h*w
areaTH = frameArea/250 #konstanta 250
print 'Area Threshold', areaTH

#Jalur atas / bawah
line_up = int(2*(h/6)) #nilai asli int(2*(h/5))
line_down   = int(3*(h/5)) #nilai asli int(3*(h/5))

up_limit =   int(1*(h/7)) #nilai asli int(1*(h/5))
down_limit = int(4*(h/5)) #nilai asli int(4*(h/5))

#Jalur kiri / kanan
line_lift = int(2*(h/6)) #nilai asli int(2*(h/5))
line_right   = int(3*(h/5)) #nilai asli int(3*(h/5))

lift_limit =   int(1*(h/7)) #nilai asli int(1*(h/5))
right_limit = int(4*(h/5)) #nilai asli int(4*(h/5))



print "Red line y:",str(line_down)
print "Blue line y:", str(line_up)
print "green line y:",str(line_lift)
print "yeloow line y:", str(line_right)

line_down_color = (255,0,0)
line_up_color = (0,0,255)

line_lift_color = (255,255,0)
line_right_color = (0,255,255)

pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-2,1,2))
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-2,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-2,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-2,1,2))
###############################################################
pt9 =  [w, line_lift]
pt10 =  [0, line_lift]
pts_L5 = np.array([pt9,pt10], np.int32)
pts_L5 = pts_L5.reshape((-1,2,1))
pt11 =  [w, line_right]
pt12 =  [0, line_right]
pts_L6 = np.array([pt11,pt12], np.int32)
pts_L6 = pts_L6.reshape((-1,2,1))

pt13 =  [0, right_limit]
pt14 =  [w, right_limit]
pts_L7 = np.array([pt13,pt14], np.int32)
pts_L7 = pts_L7.reshape((-1,2,1))
pt15 =  [0, lift_limit]
pt16 =  [w, lift_limit]
pts_L8 = np.array([pt15,pt16], np.int32)
pts_L8 = pts_L8.reshape((-1,2,1))


#Substractor de fondo
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

#Elementos estructurantes para filtros morfoogicos
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#Variables
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1



# loop runs if capturing has been initialized.
while True:
    # reads frames from a video
    ret, frames = cap.read()

    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)


    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale(gray, 1.2, 3)

    # To draw a rectangle in each cars
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y),(x+w,y+h),(255,255,0),1)

    #################
    #   IMAGANES    #
    #################
    str_up = 'Kanan: '+ str(cnt_up)
    str_down = 'Kiri: '+ str(cnt_down)
    # frames = cv2.polylines(frames,[pts_L1],False,line_down_color,thickness=2)
    # frames = cv2.polylines(frames,[pts_L2],False,line_up_color,thickness=2)
    # frames = cv2.polylines(frames,[pts_L3],False,(255,0,255),thickness=1)
    # frames = cv2.polylines(frames,[pts_L4],False,(255,0,255),thickness=1)
    cv2.putText(frames, str_up ,(10,40),font,1.5,(255,0,255),2,cv2.LINE_AA)
    cv2.putText(frames, str_up ,(10,40),font,1.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frames, str_down ,(10,90),font,1.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frames, str_down ,(10,90),font,1.5,(255,0,0),1,cv2.LINE_AA)

    # #################
    # #   IMAGANES    #
    # #################
    # str_lift = 'LIFT: '+ str(cnt_lift)
    # str_right = 'RIGHT: '+ str(cnt_right)
    # cv2.line(frames, 9, 8, [, thickness[, lineType[, shift]]])
    cv2.line(frames,(960-100,0),(960-100,1280),(255,0,0),5)
    cv2.line(frames,(320+100,0),(320+100,1280),(255,255,0),5)
    # cv2.line(frames,(0,512),(2280,1280),(255,128,0),5)
    # cv2.line(frames,(0,0),(511,511),(255,255,0),5)
    # cv2.line(frames,(0,0),(511,511),(255,0,255),5)
    # cv2.line(frames,(0,0),(511,999),(255,255,255),5)

    # frames = cv2.polylines(frames,[pts_L5],True,line_lift_color,thickness=2)
    # frames = cv2.polylines(frames,[pts_L6],True,line_right_color,thickness=2)
    # frames = cv2.polylines(frames,[pts_L7],True,(255,255,255),thickness=1)
    # frames = cv2.polylines(frames,[pts_L8],True,(255,255,255),thickness=1)
    # cv2.putText(frames, str_lift ,(50,40),font,1.5,(255,255,255),4,cv2.LINE_AA)
    # cv2.putText(frames, str_lift ,(50,40),font,1.5,(0,255,255),3,cv2.LINE_AA)
    # cv2.putText(frames, str_right ,(50,90),font,1.5,(255,255,255),4,cv2.LINE_AA)
    # cv2.putText(frames, str_right ,(50,90),font,1.5,(255,255,0),3,cv2.LINE_AA)



   # Display frames in a window
    cv2.imshow('video2', frames)

    # Wait for Esc key to stop
    if cv2.waitKey(33) == 27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()
