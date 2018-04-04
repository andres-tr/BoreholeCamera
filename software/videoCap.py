#This code is for low FPS
import cv2
import time

#Ip Camera 
vcap = cv2.VideoCapture("http://192.168.1.77/video.mjpg")
frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))

length = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
out = cv2.VideoWriter('/media/pi/HD/logvid/' + time.strftime("%d_%m_%Y_%H_%M") + '.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 6, (frame_width,frame_height))
cont = 0

while(True):
    if vcap.grab():
        ret2, frame2 = vcap.retrieve()
        #cv2.imshow('FPS', frame2)
        if cont  == 3 or cont == 6 or cont == 9:
            out.write(frame2)
            #cv2.imshow('FPS',frame2)
            print cont
        cont = cont + 1 
    if cont == 16:
        cont = 0
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

vcap.release()
out.release()
cv2.destroyAllWindows()
