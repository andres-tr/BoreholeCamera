#!/usr/bin/env python

from sensor_msgs.msg import Imu
import rospy

rospy.init_node('imu_metamotionr')

imu_pub = rospy.Publisher('imu', Imu, queue_size=50)

r = rospy.Rate(30)
while not rospy.is_shutdown():
	current_time = rospy.Time.now()
	imu_sens = Imu()
	imu_sens.header.stamp = current_time
	imu_sens.header.frame_id = "imu"
        #imu_sens.child_frame_id = "imu"
	imu_sens.orientation.x = -0.016
        imu_sens.orientation.y=-0.016
        imu_sens.orientation.z=0.99
        imu_sens.orientation.w=0.09
        imu_sens.angular_velocity.x=-0.013
        imu_sens.angular_velocity.y=-0.014
        imu_sens.angular_velocity.z=5.092
        imu_sens.linear_acceleration.x=0.11
        imu_sens.linear_acceleration.y=0.23
        imu_sens.linear_acceleration.z=11.81
	
	imu_sens.linear_acceleration_covariance = [0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001]
	imu_sens.angular_velocity_covariance = [0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001]
	imu_sens.orientation_covariance = [0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001, 0.0000001]
	imu_pub.publish(imu_sens)
	r.sleep()
