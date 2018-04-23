#!/usr/bin/env python
import rospy

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped

path = Path()

def path_callback(data):
    global path
    path.header = data.header
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose.pose
    path.poses.append(pose)
    path_pub.publish(path)

rospy.init_node('path_node')

odom_sub = rospy.Subscriber('/robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, path_callback)
path_pub = rospy.Publisher('/path', Path, queue_size=20)

if __name__ == '__main__':
    rospy.spin()
