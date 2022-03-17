#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu, MagneticField
from geometry_msgs.msg import Vector3

rospy.init_node('imu_timeout')
imu_timeout_pub = rospy.Publisher("imu/data_wtimeout", Imu, queue_size=50)
old_imu_time = 0
new_imu_time = 0

def callback(data):
    global new_imu_time, old_imu_time
    new_imu_time =  data.header.stamp.secs
    if (new_imu_time - old_imu_time) > 1:
       rospy.sleep(8)
    else:      
    	imu_timeout_pub.publish(data)
    old_imu_time = new_imu_time

def listener():
    rospy.Subscriber("imu/data", Imu, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
