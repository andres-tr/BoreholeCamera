#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

val2 = 0
delta = -0.1

def update_line(hl, new_data):
    xdata, ydata, zdata = hl._verts3d
    hl.set_xdata(list(np.append(xdata, new_data[0])))
    hl.set_ydata(list(np.append(ydata, new_data[1])))
    hl.set_3d_properties(list(np.append(zdata, new_data[2])))
    plt.draw()

def callback(data):
    global val2, delta
    val1 = data.pose.pose.position.z
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.z)
    if ((val1 - val2) <= delta):
        val2 = val1
        print "Delta achieved"
	update_line(hl, (2,2, val1))
        plt.show(block=False)
        plt.pause(0.01)

def listener():
    rospy.init_node('listZplot', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)

    rospy.spin()

if __name__ == '__main__':
    map = plt.figure()
    map_ax = Axes3D(map)
    map_ax.autoscale(enable=True, axis='both', tight=True)

    # # # Setting the axes properties
    map_ax.set_xlim3d([0.0, 10.0])
    map_ax.set_ylim3d([0.0, 10.0])
    map_ax.set_zlim3d([0.0, 10.0])

    hl, = map_ax.plot3D([0], [0], [0])

    listener()


