#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry

import cv2
from cv_bridge import CvBridge, CvBridgeError



rospy.init_node('VideoPublisher', anonymous=True)

VideoRaw = rospy.Publisher('VideoRaw', Image, queue_size=10)

#cam = cv2.VideoCapture('/home/parallels/VideoPozoElSalitre.mp4')

#Ip Camera 
vcap = cv2.VideoCapture("http://192.168.0.198/video.mjpg")
frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))

cont = 0
meters = 0.0

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %.3f", data.pose.pose.position.z)
    global meters
    meters = (data.pose.pose.position.z)*-1

def listener():
    global meters
    #rospy.init_node('listenerZvideoCap', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
       if vcap.grab():
          ret, frame = vcap.retrieve()
          text = "Metros: %.3f" % meters
          cv2.putText(frame,text,(frame_width/3,frame_height/2),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)
          msg_frame = CvBridge().cv2_to_imgmsg(frame,"bgr8")
          VideoRaw.publish(msg_frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
             vcap.release()
             out.release()
             cv2.destroyAllWindows()
             break

if __name__ == '__main__':
    listener()

'''
while cam.isOpened():
    meta, frame = cam.read()
    msg_frame = CvBridge().cv2_to_imgmsg(frame,"bgr8")
    #msg_frame =  cv_bridge.cv2_to_imgmsg(frame, encoding="passthrough")
    VideoRaw.publish(msg_frame)
    #time.sleep(0.1)
'''

