#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import Temperature
from nav_msgs.msg import Odometry
z = 0
z_old = 0
temp = 0

def odom_callback(data):
    global z, z_old
    z = data.pose.pose.position.z
    if ((z - z_old) < -0.2):
        z_old = z
        txt_out()

def temp_callback(data):
    global temp
    temp = data.temperature

def txt_out():
    print  str(temp) + ";" + str(z)
    f = open(timestr + "-temp.txt", "a")
    f.write(str(temp) +";"  +  str(z) + "\n")
    f.close()
 

rospy.init_node('listener_txtout_node')
txt_sub2 = rospy.Subscriber('/odom', Odometry, odom_callback, queue_size = 1)
txt_sub3 = rospy.Subscriber('/temp', Temperature, temp_callback, queue_size = 1)

if __name__ == '__main__':
    timestr = time.strftime("%Y-%m-%d-%H-%tr = time.strftime("%Y-%m-%d-%H-%M-%S")-%S")
    rospy.spin()

