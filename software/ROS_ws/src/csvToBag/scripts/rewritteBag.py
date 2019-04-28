#!/usr/bin/env python
import rosbag, rospy
from nav_msgs.msg import Odometry

with rosbag.Bag('/home/parallels/SanMiguelito_Odome4.bag', 'w') as outbag:
    for topic, msg, t in rosbag.Bag('/home/parallels/SanMiguelito_Odom4.bag').read_messages():
        # This also replaces tf timestamps under the assumption 
        # that all transforms in the message share the same timestamp
        if topic == "/odom":
	    #print msg.pose.pose.position.x*-1
            msg.pose.pose.position.z = msg.pose.pose.position.z*-1
            #msg.header.stamp.secs = rospy.Time.from_sec(msg.header.stamp.secs + 5793212)
	   #           msg.header.stamp.secs = msg.header.stamp.secs + 5771610 + 21602
            #          msg.header.stamp.nsecs = msg.header.stamp.nsecs + 275955000 + 38000000
            #print t
            outbag.write(topic, msg, t)


