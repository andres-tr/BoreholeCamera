#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu, MagneticField
from geometry_msgs.msg import Vector3

rospy.init_node('lsm9ds1_calibration')

def callback(data):
    rospy.set_param('/imu/x_cal', data.linear_acceleration.x*-1)
    rospy.set_param('/imu/y_cal', data.linear_acceleration.y*-1)
    rospy.set_param('/imu/z_cal', data.linear_acceleration.z*-1)    
    rospy.signal_shutdown("Calibration Finished")    
 
def listener():

    rospy.Subscriber("imu/data_raw", Imu, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()


