#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import Imu
import csv
from geometry_msgs.msg import Vector3

#Convert G to m/s
def convert_accel(float_G):
	return float_G/0.101972

#Convert acceleration from deg/s to rad/s
def convert_gyro(float_gyro):
	return  float_gyro/57.295779

with open("/home/parallels/Gyro_X.csv", "r") as f:
	i = 0
	with rosbag.Bag('/home/parallels/Gyro_X.bag', 'w') as bag:
		reader = csv.reader(f)
		for row in reader:
			msg = Imu()
			t = rospy.Time(1526707104.251 + float(row[2]))
			msg.header.stamp = t
			msg.angular_velocity = Vector3(convert_gyro(float(row[3])), convert_gyro(float(row[4])),convert_gyro(float(row[5])))
			bag.write('imu_gyro', msg, t)
			

