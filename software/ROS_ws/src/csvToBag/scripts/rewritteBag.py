#!/usr/bin/env python
import rosbag
from nav_msgs.msg import Odometry

with rosbag.Bag('/home/parallels/Odom_ValleVide.bag', 'w') as outbag:
    for topic, msg, t in rosbag.Bag('/home/parallels/Odom_ValleVid.bag').read_messages():
        # This also replaces tf timestamps under the assumption 
        # that all transforms in the message share the same timestamp
        if topic == "/odom":
	    #print msg.pose.pose.position.x*-1
            msg.pose.pose.position.z = msg.pose.pose.position.z*-1
            outbag.write(topic, msg, t)


