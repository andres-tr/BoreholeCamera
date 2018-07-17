#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import cv2
import time
meters = 0.0


#Ip Camera 
vcap = cv2.VideoCapture("http://192.168.0.101/video.mjpg")
frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))

length = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
#out = cv2.VideoWriter('/media/' + time.strftime("%d_%m_%Y_%H_%M") + '.avi',cv2.VideoWriter_fourcc(*'MPEG'), 6, (frame_width,frame_height))
out = cv2.VideoWriter(time.strftime("%d_%m_%Y_%H_%M") + '.avi',cv2.VideoWriter_fourcc(*'MPEG'), 6, (frame_width,frame_height))

cont = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.pose.pose.position.x)
    global meters
    meters = data.pose.pose.position.x

def listener():
    global meters
    rospy.init_node('listenerZvideoCap', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
       if vcap.grab():
          ret, frame = vcap.retrieve()
          text = "Metros: " + str(meters)
          cv2.putText(frame,text,(frame_width/3,frame_height/2),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)
          cv2.imshow('CAM', frame)
          out.write(frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
             vcap.release()
             out.release()
             cv2.destroyAllWindows()
             break

if __name__ == '__main__':
    listener()


'''
For lees frames than original video
    if vcap.grab():
        ret2, frame2 = vcap.retrieve()
        #cv2.imshow('FPS', frame2)
        if cont  == 3 or cont == 6 or cont == 9:
            out.write(frame2)
            cv2.imshow('FPS',frame2)
            print cont
        cont = cont + 1 
    if cont == 16:
        cont = 0
'''    

