# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV
##Contador de personas
##Federico Mejia
import numpy as np
import cv2
import time
# import firebase
import serial

cnt_up   = 0
cnt_down = 0












# capture frames from a video
cap = cv2.VideoCapture("VID_20181029_095024.mp4")

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('cars.xml')





#Cetak properti pengambilan ke konsol
for i in range(19): #range asli 19
    print i, cap.get(i)

w = cap.get(3) #nilai asli 3
h = cap.get(4) #nilai asli 4
framesArea = 2*(h*w) #nilai asli h*w
areaTH = framesArea/250 #konstanta 250
print 'Area Threshold', areaTH

#Jalur masuk / keluar
line_up = int(2*(h/6)) #nilai asli int(2*(h/5))
line_down   = int(3*(h/5)) #nilai asli int(3*(h/5))

up_limit =   int(1*(h/7)) #nilai asli int(1*(h/5))
down_limit = int(4*(h/5)) #nilai asli int(4*(h/5))

print "Red line y:",str(line_down)
print "Blue line y:", str(line_up)
line_down_color = (255,0,0)
line_up_color = (0,0,255)
pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

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
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    # To draw a rectangle in each cars
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)

    #########################
    #   PRE-PROCESAMIENTO   #
    #########################

    #Aplica substraccion de fondo
    fgmask = fgbg.apply(frames)
    fgmask2 = fgbg.apply(frames)

    #Binariazcion para eliminar sombras (color gris)
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2 = cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
        #Opening (erode->dilate) para quitar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regiones blancas.
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print 'UP:',cnt_up
        print 'DOWN:',cnt_down
        break
    #################
    #   CONTORNOS   #
    #################

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:
            #################
            #   TRACKING    #
            #################

            #Falta agregar condiciones para multipersonas, salidas y entradas de pantalla.

            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit):
                for i in persons:
                    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                        # el objeto esta cerca de uno que ya se detecto antes
                        new = False
                        i.updateCoords(cx,cy)   #actualiza coordenadas en el objeto and resets age
                        if i.going_UP(line_down,line_up) == True:
                            cnt_up += 1;
                            # print "ID:",i.getId(),'crossed going up at',time.strftime("%c")
                            print "Masuk: ", cnt_up, "\t|\tTotal di ruangan: ", cnt_up-cnt_down, "\t|\tPada tanggal :", time.strftime("%a, %d %b %Y"), "\t|\tPada Jam :", time.strftime("%H:%M:%S")
                            # print getArduino()
                        elif i.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1;
                            # print "ID:",i.getId(),'crossed going down at',time.strftime("%c")
                            print "Keluar: ", cnt_down, "\t|\tTotal di ruangan: ", cnt_up-cnt_down, "\t|\tPada tanggal :", time.strftime("%a, %d %b %Y"), "\t|\tPada Jam :", time.strftime("%H:%M:%S")
                            # print getArduino()
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        #sacar i de la lista persons
                        index = persons.index(i)
                        persons.pop(index)
                        del i     #liberar la memoria de i
                # if new == True:
                    # p = Person.MyPerson(pid,cx,cy, max_p_age)
                    # persons.append(p)
                    # pid += 1
            #################
            #   DIBUJOS     #
            #################
            cv2.circle(frames,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frames,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.drawContours(frames, cnt, -1, (0,255,0), 3)

    #END for cnt in contours0

    #########################
    # DIBUJAR TRAYECTORIAS  #
    #########################
    for i in persons:
    ##        if len(i.getTracks()) >= 2:
    ##            pts = np.array(i.getTracks(), np.int32)
    ##            pts = pts.reshape((-1,1,2))
    ##            frames = cv2.polylines(frames,[pts],False,i.getRGB())
    ##        if i.getId() == 9:
    ##            print str(i.getX()), ',', str(i.getY())
        cv2.putText(frames, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)

    #################
    #   IMAGANES    #
    #################
    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    frames = cv2.line(frames,[pts_L1],False,line_down_color,thickness=2)
    frames = cv2.line(frames,[pts_L2],False,line_up_color,thickness=2)
    frames = cv2.line(frames,[pts_L3],False,(255,255,255),thickness=1)
    frames = cv2.line(frames,[pts_L4],False,(255,255,255),thickness=1)
    cv2.putText(frames, str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frames, str_up ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frames, str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frames, str_down ,(10,90),font,0.5,(255,0,0),1,cv2.LINE_AA)

    cv2.imshow('frames',frames)

   # Display frames in a window
    # cv2.imshow('video2', frames)

    # Wait for Esc key to stop
    if cv2.waitKey(33) == 27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()
