#!/usr/bin/env python
import rospy
import time
import math
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Pose2D

x = 0.0001
y = 0.0001

def pose_callback(data):
    global x,y
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    r = math.sqrt(math.pow(x,2)+ math.pow(y,2))
    polar_data.x= r
    #print "r: " + str(r) + " x: " + str(x) + " y: " + str(y)
    theta = math.degrees(math.atan(y/x))
    #print "theta: " + str(theta)
    polar_pub.publish(polar_data) 
    polar_data.theta = theta

rospy.init_node('polar_publisher')
polar_sub = rospy.Subscriber('/robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, pose_callback, queue_size = 1)
polar_pub = rospy.Publisher("pose/polar", Pose2D, queue_size=10)
polar_data = Pose2D()
if __name__ == '__main__':
    rospy.spin()




