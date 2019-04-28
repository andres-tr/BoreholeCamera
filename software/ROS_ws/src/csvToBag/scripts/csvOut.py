#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

def callback_pose(data):
    print str(data.header.stamp.secs) + ";" + str(data.pose.pose.position.x) + ";" + str(data.pose.pose.position.y) + ";" + str(data.pose.pose.position.z) + ";" + str(data.pose.pose.orientation.x) + ";" + str(data.pose.pose.orientation.y) + ";" + str(data.pose.pose.orientation.z) + ";" + str(data.pose.pose.orientation.w)
    rospy.sleep(5.2)

def listener_csvout():
    rospy.init_node('listener_csvout', anonymous=True)
    rospy.Subscriber("/robot_pose_ekf/odom_combined", PoseWithCovarianceStamped, callback_pose, queue_size = 1)
    rospy.queue_size = None 
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    #rospy.Timer(rospy.Duration(2), callback_pose, oneshot=False)
    #rospy.sleep(10.)
    while not rospy.is_shutdown():
    	rospy.sleep(1.9)



if __name__ == '__main__':
    msg = PoseWithCovarianceStamped()
    listener_csvout()
