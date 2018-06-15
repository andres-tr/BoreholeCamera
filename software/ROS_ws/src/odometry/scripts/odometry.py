#!/usr/bin/env python
import math

import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

rospy.init_node('odometry_publisher')

odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
odom_broadcaster = tf.TransformBroadcaster()

input_A = 18
input_B = 23

lastEncoderValue = 0
encoderValue = 0

lastEncoded = 0
lastx = 0

x = 0.0
y = 0.0
z = 0.0

vx = 0.0
vy = 0.0
vz = 0.0

current_time = rospy.Time.now()
last_time = rospy.Time.now()

# GPIO Setup
GPIO.setup(input_A, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(input_B, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


# interrupt Service Routine
def updateEncVal(channel):
    global  lastEncoded, lastEncoderValue, encoderValue, current_time, last_time, x, y, z, vx, vy,vz
   
    # obtain time and time elapsed 
    #current_time = rospy.Time.now()
    #dt = (current_time - last_time).to_sec()

    # read Encoder pins, from encoder position determine direction
    MSB = GPIO.input(input_A)
    LSB = GPIO.input(input_B)
    encoded = (MSB << 1)| LSB
    suma  = (lastEncoded << 2) | encoded 
    if suma == 13 or suma == 4 or suma == 2 or suma == 11:
        encoderValue = encoderValue +1
    if suma == 14 or suma == 7 or suma == 1 or suma == 8:
        encoderValue= encoderValue -1
    lastEncoded = encoded    

    # compute distance
    x = (encoderValue*0.3330096)/800

    # velocity
    
    #de = encoderValue - lastEncoderValue
    #lastEncoderValue = encoderValue
    #vx = de/dt
    #last_time = current_time


# attach interrupt
GPIO.add_event_detect(input_A, GPIO.BOTH, callback = updateEncVal)
GPIO.add_event_detect(input_B, GPIO.BOTH, callback = updateEncVal)


rate = rospy.Rate(25) # 10hz

while True:

    #since all odometry is 6DOF we'll need a quaternion created from yaw
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, 0)

    #first, we'll publish the transform over tf
    odom_broadcaster.sendTransform(
        (x, y, z),
        odom_quat,
        current_time,
        "base_link",
        "odom"
    )

    # next, we'll publish the odometry message over ROS
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set time
    current_time = rospy.Time.now()
    dt = (current_time - last_time).to_sec()

    # set the position
    odom.pose.pose = Pose(Point(x, y, z), Quaternion(*odom_quat))

    odom.pose.covariance = [0.0000000001,  0.0,  0.0,  0.0,  0.0,  0.0, 
			    0.0,   99999, 0.0,  0.0,  0.0,  0.0, 
			    0.0,   0.0, 99999,  0.0,  0.0,  0.0, 
			    0.0,   0.0,  0.0,  99999,  0.0,  0.0, 
			    0.0,   0.0,  0.0,  0.0,  99999,  0.0, 
			    0.0,   0.0,  0.0,  0.0,  0.0,  99999]

    # velocity    
    dx = x - lastx
    lastx = x
    vx = dx/dt
    last_time = current_time

    # set the velocity
    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(vx, vy, vz), Vector3(0, 0, 0))

    # publish the message
    odom_pub.publish(odom)

    rate.sleep()
