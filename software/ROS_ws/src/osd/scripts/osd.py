#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import cv2
import time

#Ip Camera 
vcap = cv2.VideoCapture("http://192.168.1.77/video.mjpg")
frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))

out = cv2.VideoWriter('/media/pi/HD/logvid/' + time.strftime("%d_%m_%Y_%H_%M") + '.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 6, (frame_width,frame_height))
cont = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.pose.pose.position.z)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("odom", Odometry, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
