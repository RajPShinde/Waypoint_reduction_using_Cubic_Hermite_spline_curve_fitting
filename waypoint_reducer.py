#!/usr/bin/python2.7

import roslib
import matplotlib.pyplot as plot
import rospy
from geometry_msgs.msg import PoseStamped
import numpy as np
import math

points=[]

# Take Input form user
def take_input():
    flag=1
    while flag==1:    
      N=input("Enter the number of Points (N):")
      N=int(N)
      if N>0 and N<993:
          flag=0
      else:
          print("Please input a number between 0 and 992. Try Again!")
    return N

# Callback for listning waypoints
def callback(msg):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    euler = tf.transformations.euler_from_quaternion([0, 0, msg.pose.orientation.z, msg.pose.orientation.w])
    #slope=math.atan(yaw)
    print(euler)
    slope=10
    points.append([msg.pose.position.x,msg.pose.position.y])
    slopes.append(slope)
    print(points)
    print(slopes)
      
# Draw the Paths
def draw_path(path):

    # Plot original Waypoints
    points= [[1,1],[4,5],[5,4],[6,8],[8,9]]
    points.sort()
    plot.subplot(212)
    plot.plot([p[0] for p in points], [p[1] for p in points], 'o')
    plot.show(block=False)
    
    # Select N waypoints

    # Plot N waypoints and a path using Cubic Hermite Spline curve fitting Method
    points= [[1,1],[4,5],[5,4],[6,8],[8,9]]
    points.sort()
    plot.figure(1)
    plot.subplot(211)
    N=3
    plot.plot([p[0] for p in points], [p[1] for p in points], 'o')
    M=np.array([[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]])
    for i in range(N+1):
        
        diff=points[i+1][0]-points[i][0]
        print(diff)
        G=np.array([[points[i][1]],[points[i+1][1]],[slope1*diff],[slope2*diff]])
    
        # Polynomial Weights
        V=np.matmul(M,G)
        print(V)
    
        X=[]
        Y=[]
    

        # Plot  New Path
        for x in np.arange(0, 1, 0.001):
          y= (V[0][0]*x*x*x)+(V[1][0]*x*x)+(V[2][0]*x)+V[3][0]
          # Remap from 0-1 to x1-x2
          x=points[i][0]+(diff*x)
          X.append(x)
          Y.append(y)
      
        plot.plot(X,Y)
    plot.show()

def listener():
    rospy.init_node('waypoint_reducer', anonymous=True)
    rospy.Subscriber("/vslam2d_pose", PoseStamped, callback)
    waypoint = PoseStamped()
    rospy.spin()
    print("Waiting for rosbag to finish playing...")
    if len(points)==992:
        take_input()
        draw_path(points)
        

listener()
