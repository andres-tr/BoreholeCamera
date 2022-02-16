#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Temperature
from nav_msgs.msg import Odometry
global z

def callback_pose(data):
    global z
    print str(data.header.stamp.secs) + ";" + str(data.temperature) + ";" + str(z)
    rospy.sleep(5.2)

def callback_odome(data):
    global z
    z = data.pose.pose.position.z

def listener_csvout():
    rospy.init_node('listener_csvout', anonymous=True)
    rospy.Subscriber("/temp", Temperature, callback_pose, queue_size = 1)
    rospy.Subscriber("/odom", Odometry,callback_odome, queue_size=1)
    rospy.queue_size = None
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    #rospy.Timer(rospy.Duration(2), callback_pose, oneshot=False)
    #rospy.sleep(10.)
    while not rospy.is_shutdown():
        rospy.sleep(1.9)



if __name__ == '__main__':
    msg = Temperature()
    listener_csvout()

