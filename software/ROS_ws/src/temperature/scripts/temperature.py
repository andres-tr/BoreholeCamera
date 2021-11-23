#!/usr/bin/python
import tsys01
from time import sleep

sensor = tsys01.TSYS01()

import rospy
from sensor_msgs.msg import Temperature

#Init Node temp
temp_pub = rospy.Publisher('temp', Temperature, queue_size=50)
rospy.init_node('temp', anonymous=True)
r = rospy.Rate(10) # 10hz

if not sensor.init():
	print("Error initializing sensor")
	exit(1)

while not rospy.is_shutdown():
	if not sensor.read():
        	print("Error reading sensor")
        	exit(1)
	temp_sens = Temperature()
	temp_sens.header.stamp = rospy.Time.now()
	temp_sens.header.frame_id = "temp"	
	temp_sens.temperature = sensor.temperature()
	temp_pub.publish(temp_sens)
	#rospy.loginfo(temp_sens)
	r.sleep()


