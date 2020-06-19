# Waypoint reduction using Cubic Hermite spline curve fitting
[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/RajPShinde/waypoint_reducer/blob/master/LICENSE)

## Authors
* **Raj Prakash Shinde** [GitHub](https://github.com/RajPShinde)

## Description
A python script to reduce the way points for a robot while still trying to retain the original path trajectory

## Dependencies
1. Ubuntu 16.04+
2. python 2.7
3. ROS Kinetic+
4. OpenCV 
5. Numpy
6. Matplotlib

## Approach
TBW

## Build
Steps to build
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
source devel/setup.bash
cd src/
git clone https://github.com/RajPShinde/waypoint_reducer
cd waypoint_reducer/scripts
chmod gu+x waypoint_reducer.py
cd ~/catkin_ws/
catkin_make
```
## Run
**Run Rosmaster**
<br> Open a new Terminal using Ctrl+T
```
roscore
```

**Run Script**
<br> Open a new Terminal using Ctrl+T (i.e make sure you are in catkin_ws directory)
```
source devel/setup.bash
rosrun waypoint_reducer waypoint_reducer.py
```

**Run Bag File**
<br>**Note**- Make sure the bag File for the waypoint reducuction question is already present in the catkin_ws folder
<br> Open a new Terminal using Ctrl+T (i.e make sure you are in catkin_ws directory)
```
rosbag play path_test.bag
```