#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import Temperature
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
z_odom = 0
z_old = 0
x = 0 
y = 0
z = 0

def odom_callback(data):
    global z_odom, z_old
    z_odom = data.pose.pose.position.z
    if ((z_odom - z_old) < -0.2):
        z_old = z_odom
        txt_out()

def pose_callback(data):
    global x,y,z
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    z = data.pose.pose.position.z


def txt_out():
    print  str(x) + ";" + str(y) + ";"+ str(z) + ";" + str(z_odom)
    f = open(timestr + "-pose.txt", "a")
    f.write(str(x) + ";" + str(y) + ";"+ str(z) + ";" +  str(z_odom) + "\n")
    f.close()

rospy.init_node('listener_txt_pose_node')
txt_sub4 = rospy.Subscriber('/odom', Odometry, odom_callback, queue_size = 1)
txt_sub5 = rospy.Subscriber('/robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, pose_callback, queue_size = 1)

if __name__ == '__main__':
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
    rospy.spin()
