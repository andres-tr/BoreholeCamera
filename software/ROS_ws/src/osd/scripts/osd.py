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
cont = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.pose.pose.position.z)
    global meters 
    meters = data.pose.pose.position.z
    
def listener():
    global meters
    rospy.init_node('listenerZ', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
       ret, frame = vcap.read()
       text = "Metros: " + str(meters) 
       cv2.putText(frame,text,(frame_width/3,frame_height/2),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)
       cv2.imshow('CAM', frame)
       if cv2.waitKey(1) & 0xFF == ord('q'):
          break
       vcap.release()
       out.release()
       cv2.destroyAllWindows()
 

if __name__ == '__main__':
    listener()
