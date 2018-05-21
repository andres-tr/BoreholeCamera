#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3

def callback_acc(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.linear_acceleration.x)    
    msg.header.stamp = data.header.stamp
    msg.linear_acceleration = Vector3(data.linear_acceleration.x, data.linear_acceleration.y , data.linear_acceleration.z)
    pub.publish(msg)

def callback_gyro(data):
    msg.header.stamp = data.header.stamp
    msg.angular_velocity = Vector3(data.angular_velocity.x, data.angular_velocity.y , data.angular_velocity.z)
    pub.publish(msg)

def listener_imu():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener_imu', anonymous=True)

    rospy.Subscriber("imu_acc", Imu, callback_acc)
    rospy.Subscriber("imu_gyro", Imu, callback_gyro)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    msg = Imu()
    msg.angular_velocity = Vector3(0.0000001,0.0000001,0.0000001)
    msg.linear_acceleration = Vector3(0.0000001,0.0000001,0.0000001)
    msg.header.frame_id = "base_footprint"
    pub = rospy.Publisher('imu/data_raw', Imu, queue_size=10)
    listener_imu()


