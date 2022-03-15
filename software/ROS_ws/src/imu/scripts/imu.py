#!/usr/bin/env python

import smbus
import time
import numpy
import math

import rospy
from sensor_msgs.msg import Imu, MagneticField
from geometry_msgs.msg import Vector3

#ACC deviation variables
x_cal = 0.0
y_cal = 0.0
z_cal = 0.0

#  IMU Magnetometer address  0x1e
m_add = 0x1e

# IMU Acc and Gyro address 0x6b 
ag_add =0x6b

# Initialize I2C (SMBus)
bus = smbus.SMBus(1)

# Verify comunication Magnetometer
if bus.read_byte_data(m_add , 0x0F) == 0x3D:
	print "Mag ready"
else:
	print "Mag not ready"

# Verify comunication Acc and Gyro
if bus.read_byte_data(ag_add , 0x0F) == 0x68:
        print "Acc and Gyro ready"
else:
        print "Acc and Gyro not ready"

#Init Gyro
#CTRL_REG1_G
bus.write_byte_data(ag_add, 0x10, 0xC0)
#CTRL_REG2_G
bus.write_byte_data(ag_add, 0x11, 0x00)
#CTRL_REG3_G
bus.write_byte_data(ag_add, 0x12, 0x00)
#CTRL_REG4
bus.write_byte_data(ag_add, 0x1E, 0x3A)
#ORIENT_CFG_G
bus.write_byte_data(ag_add, 0x13, 0x00)

#Init Accel
#CTRL_REG5_XL
bus.write_byte_data(ag_add, 0x1F, 0x38)
#CTRL_REG6_XL
bus.write_byte_data(ag_add, 0x20, 0xC0)
#CTRL_REG7_XL
bus.write_byte_data(ag_add, 0x21, 0x00)

#Init MAG
#CTRL_REG1_M
bus.write_byte_data(m_add, 0x20, 0x7C)
#CTRL_REG2_M
bus.write_byte_data(m_add, 0x21, 0x00)
#CTRL_REG3_M
bus.write_byte_data(m_add, 0x22, 0x00)
#CTRL_REG4_M
bus.write_byte_data(m_add, 0x23, 0x0C)
#CTRL_REG5_M
bus.write_byte_data(m_add, 0x24, 0x00)

#Init variables
heading = 0.0

#ROS init
rospy.init_node('lsm9ds1_sensor')
imu_pub = rospy.Publisher("imu/data_raw", Imu, queue_size=50)
imu_pub2 = rospy.Publisher("imu/mag", MagneticField, queue_size=50)
rate = rospy.Rate(25) # 10hz

#Convert G to m/s
def convert_accel(float_G):
	return float_G/0.101972

#Convert acceleration from deg/s to rad/s
def convert_gyro(float_gyro):
	return  float_gyro/57.295779

#Convert Gauss to Teslas
def convert_gauss(float_teslas):
	return float_teslas*0.0001

while not rospy.is_shutdown():
	#ROS imu msg init
	imu_msg = Imu()
	imu_msg.header.stamp = rospy.Time.now()
        x_cal = rospy.get_param('imu/x_cal')
        y_cal = rospy.get_param('imu/y_cal')
        z_cal = rospy.get_param('imu/z_cal')
       
        print x_cal
	#Check if Gyro is available
	byte = bus.read_byte_data(ag_add , 0x17)
	if byte == 7:
		gyro = bus.read_i2c_block_data(ag_add,0x18,6)
                if len(gyro) == 6:
                        xgyro = (gyro[1] << 8) | gyro[0]
			xgyro = float(numpy.int16(xgyro))*0.00875
                        ygyro = (gyro[3] << 8) | gyro[2]
			ygyro = float(numpy.int16(ygyro))*0.00875
                        zgyro = (gyro[5] << 8) | gyro[4]
			zgyro = float(numpy.int16(zgyro))*0.00875
			#Twos complement * scale
                        #print "Gyro x:" + str(xgyro) + " y:" + str(ygyro) + " z: " + str(zgyro)
			imu_msg.angular_velocity = Vector3(convert_gyro(xgyro), convert_gyro(ygyro),convert_gyro(zgyro))
			imu_msg.angular_velocity_covariance =  [0.00000, 0.0, 0.0, 0.00000, 0.0, 0.0, 0.00000, 0.0, 0.0]
			#imu_pub.publish(imu_msg)
	else:
		print "No entre"
	
	#Check if Acc is available
        byte = bus.read_byte_data(ag_add , 0x27)
        if (byte & (1<<0)):
                acc = bus.read_i2c_block_data(ag_add,0x28,6)
		if len(acc) == 6:
			xacc = (acc[1] << 8) | acc[0]
			xacc = float(numpy.int16(xacc))*0.000061 + x_cal
			yacc = (acc[3] << 8) | acc[2] 
			yacc = float(numpy.int16(yacc))*0.000061 + y_cal
			zacc = (acc[5] << 8) | acc[4]
			zacc = float(numpy.int16(zacc))*0.000061 + z_cal
			#Twos complement * scale
			#print "Acc x:" + str(float(numpy.int16(xacc))*0.000732) + " y:" + str(float(numpy.int16(yacc))*0.000732) + " z: " + str(float(numpy.int16(zacc))*0.000732)
			imu_msg.linear_acceleration = Vector3(convert_accel(xacc), convert_accel(yacc),convert_accel(zacc))
                        imu_msg.linear_acceleration_covariance =  [0.00000, 0.0, 0.0, 0.00000, 0.0, 0.0, 0.00000, 0.0, 0.0]
			imu_msg.orientation_covariance =  [-1, 0.0, 0.0, 0.00000, 0.0, 0.0, 0.00000, 0.0, 0.0]
			#imu_pub.publish(imu_msg)
	
	imu_msg.header.frame_id = "imu"	
	#Publish the imu message
        imu_pub.publish(imu_msg)

	#ROS Magnetic Field msg init	
	mag_msg = MagneticField()
	mag_msg.header.stamp = rospy.Time.now()
	
	#Check if Mag is available
        byte = bus.read_byte_data(m_add , 0x27)
        if (byte & (1<<0)):
                mag = bus.read_i2c_block_data(m_add,0x28,6)
                if len(mag) == 6:
                        xmag = (mag[1] << 8) | mag[0]
			xmag = float(numpy.int16(xmag))*0.00014
                        ymag = (mag[3] << 8) | mag[2]
			ymag = float(numpy.int16(ymag))*0.00014
                        zmag = (mag[5] << 8) | mag[4]
			zmag = float(numpy.int16(zmag))*0.00014
			
			mag_msg.magnetic_field = Vector3(convert_gauss(xmag), convert_gauss(ymag),convert_gauss(zmag))			

			#print "Mag x:" + str(float(numpy.int16(xmag))*0.00014) + " y:" + str(float(numpy.int16(ymag))*0.00014) + " z: " + str(float(numpy.int16(zmag))*0.00014) + " Heading: " + str(heading)
			#Publish the Mag message
			imu_pub2.publish(mag_msg)
    	rate.sleep()
	

