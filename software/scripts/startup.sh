#!/bin/bash

echo"launchyyy entered"

export ROS_HOSTNAME=`hostname`.local
export ROS_MASTER_URI=http://winch.local:11311

source /opt/ros/kinetic/setup.bash
source /home/ubuntu/catkin_ws/devel/setup.bash

roslaunch rosbridge_server rosbridge_websocket.launch

echo"launchyyy exwcuted"




