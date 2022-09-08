#!/usr/bin/env python

import rospy
import time
import tf
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

euler_msg = Point()

def pose_callback(data):
        
    quaternion = (
    data.pose.pose.orientation.x,
    data.pose.pose.orientation.y,
    data.pose.pose.orientation.z,
    data.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    print str(euler[0]) + ' ' + str(euler[1]) + ' '+ str(euler[2])

    euler_msg.x = euler[0]
    euler_msg.y = euler[1]
    euler_msg.z = euler[2]

    euler_pub.publish(euler_msg)

#subscribe to imu_filter

rospy.init_node('quat_euler')
telemetry_sub = rospy.Subscriber('/robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, pose_callback, queue_size = 1)

euler_pub = rospy.Publisher('/euler', Point, queue_size=1)



if __name__ == '__main__':
    rospy.spin()


