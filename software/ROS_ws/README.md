## Install Workspace
```
$ cd ~
$ git clone ..
$ cd ~/ROS-Workspace
$ rosdep install --from-paths . --ignore-src --rosdistro kinetic
$ catkin_make
```

## Winch commands
```
$ sudo ntpdate time.nist.gov
$ timedatectl status
$ roscore&
$ rosrun odometry odometry.py
$ sudo ifconfig enxb827eb180ec4  down 
$ sudo ifconfig enxb827eb180ec4  up
$ sudo ifconfig wlan0 down
$ sudo ifconfig wlan0 up
```
bashrc
```
$ source /opt/ros/kinetic/setup.bash
$ source BoreholeCamera/software/ROS_ws/devel/setup.bash  
```


## Master commands
```
$ rosparam set use_sim_time true
```




