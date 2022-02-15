#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import Imu, MagneticField


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.magnetic_field.x)
    plt.scatter(data.magnetic_field.x, data.magnetic_field.y)
    plt.draw()
    #plt.pause(0.00001)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('mag_cali', anonymous=True)

    rospy.Subscriber("/imu/mag", MagneticField, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    plt.show(block=True)

if __name__ == '__main__':
    plt.axis([-0.0001, 0.0001, -0.0001, 0.0001])
    listener()
