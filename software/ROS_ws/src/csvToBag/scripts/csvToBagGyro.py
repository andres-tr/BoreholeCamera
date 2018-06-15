#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import Imu
import csv
from geometry_msgs.msg import Vector3
import math

#Convert G to m/s
def convert_accel(float_G):
	return float_G/0.101972

#Convert acceleration from deg/s to rad/s
def convert_gyro(float_gyro):
	return  float_gyro/57.295779

with open("/home/parallels/Gyro_C.csv", "r") as f:
	i = 0
	with rosbag.Bag('/home/parallels/Gyro_C.bag', 'w') as bag:
		reader = csv.reader(f)
		for row in reader:
			msg = Imu()
			dec, ent = math.modf(float(row[0])*0.001)
			#print '%.3f'% (float(row[0])*0.001)
			#t = rospy.Time(1527696243, 701000000 + int(float(row[2])*10000000000) )
			#t = rospy.Time.from_sec(float('%.3f'% (float(row[0])*0.001)))
			t = rospy.Time.from_sec(float(row[0])*0.001)
			msg.header.stamp = t
			msg.angular_velocity = Vector3(convert_gyro(float(row[3])), convert_gyro(float(row[4])),convert_gyro(float(row[5])))
			bag.write('imu_gyro', msg, t)
			

