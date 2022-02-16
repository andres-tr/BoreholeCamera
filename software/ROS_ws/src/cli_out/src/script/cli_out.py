#!/usr/bin/env python
import rospy, os
from terminalplot import plot, get_terminal_size
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Temperature


x = 0 
y = 0 
z = 0 
z_odom = 0 
z_old = 0
z_vel = 0
temp = 0
x_plot1 =[]
z_plot1 =[]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pose_callback(data):
    global x, y, z
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    z = data.pose.pose.position.z

def temp_callback(data):
    global temp
    temp = data.temperature

def odom_callback(data):
    global z_odom, z_old, z_vel
    z_odom = data.pose.pose.position.z
    z_vel = (data.twist.twist.linear.z*-60)
    if ((z_odom - z_old) < -0.2):
	z_old = z_odom
	cli_out()

def cli_out():
    global x, y, z, z_odom, z_vel, temp, x_plot1, z_plot1
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Norte: " + str(round(x,3)) + " m  "+ " Este: " + str (round(y,3)) + " m  " + " Profundidad: " + str (round(z_odom,3))
    print str(round(z_vel,3)) + " metros/min " + " Temp: " +str (round(temp,3)) + "C"  
    if temp> 0 :
	z_plot1.append(round(temp,2))
    x_plot1.append(round(z_odom,2)*-1)
    size = get_terminal_size()
    print(bcolors.OKGREEN + "Grafica Temperatura vs metros de profundidad" + bcolors.ENDC)
    plot( x_plot1, z_plot1, rows=size[0]-3, columns=size[1]-3)

rospy.init_node('cli_out_node')
cli_out_sub = rospy.Subscriber('/robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, pose_callback)
cli_out_sub2 = rospy.Subscriber('/odom', Odometry, odom_callback)
cli_out_sub3 = rospy.Subscriber('/temp', Temperature, temp_callback)

if __name__ == '__main__':
    rospy.spin()

