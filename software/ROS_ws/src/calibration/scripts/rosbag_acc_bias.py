#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu, MagneticField
from geometry_msgs.msg import Vector3

rospy.init_node('lsm9ds1_calibration')
imu_bias_pub = rospy.Publisher("imu/data_wbias", Imu, queue_size=50)

def callback(data):
    data.linear_acceleration.x = data.linear_acceleration.x + rospy.get_param('/imu/acc_bias_x')
    data.linear_acceleration.y = data.linear_acceleration.y + rospy.get_param('/imu/acc_bias_y')
    data.linear_acceleration.z = data.linear_acceleration.z + rospy.get_param('/imu/acc_bias_z')
    imu_bias_pub.publish(data)
    

def listener():
    rospy.Subscriber("imu/data_raw", Imu, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
