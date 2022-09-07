#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import Imu, MagneticField


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.magnetic_field.x)
    plt.scatter(data.magnetic_field.x + rospy.get_param("/imu_filter_node/mag_bias_x") , data.magnetic_field.y + rospy.get_param("/imu_filter_node/mag_bias_y"))
    plt.draw()
    #plt.pause(0.00001)

def listener():
    rospy.init_node('mag_corrob', anonymous=True)

    rospy.Subscriber("/imu/mag", MagneticField, callback)
    x1, y1 = [-1, 1], [0,0]
    x2, y2 = [0, 0], [-1,1]
    plt.plot(x1, y1, x2, y2, marker = 'o')
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    plt.show(block=True)

if __name__ == '__main__':
    plt.axis([-0.0001, 0.0001, -0.0001, 0.0001])
    listener()
