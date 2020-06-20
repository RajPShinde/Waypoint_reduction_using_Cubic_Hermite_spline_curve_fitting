#!/usr/bin/python2.7

import roslib
import matplotlib.pyplot as plot
import rospy
import tf.transformations
from geometry_msgs.msg import PoseStamped
import numpy as np
import math

points=[]
slopes=[]
angles=[]

# Take Input form user
def take_input():
    flag=1
    while flag==1:    
      N=input("Enter the number of Points (N):")
      N=int(N)
      if N>0 and N<len(points)+1:
          flag=0
      else:
          print("Please input a number between 0 and 992. Try Again!")
    return N

# Callback for listning waypoints
def callback(msg):
    # Quartenion to euler angle conversion
    euler = tf.transformations.euler_from_quaternion([0, 0, round(msg.pose.orientation.z,2), round(msg.pose.orientation.w,2)])
    # Obtaining a unit tangent for robot orientation
    points.append([msg.pose.position.x,msg.pose.position.y])
    slopes.append([math.cos(euler[2]),math.sin(euler[2])])
    angles.append(euler[2])
    print(len(points))
    if len(points)>991: 
        draw_path(points)

# Draw the Paths
def draw_path(points):
    while True:
        N=take_input()

        # Append the start point x,y and slope
        Npoints=[points[0]]
        Nslopes=[slopes[0]]

        # Select N waypoints
        # Divide path into N+1 Parts
        division=int(math.floor(len(points)/(N+1)))
        j=1
        while len(Npoints)!=N+1:
            indice=division*j
            j=j+1
            Npoints.append(points[indice]) 
            Nslopes.append(slopes[indice])

        # Append the goal point x,y and slope
        Npoints.append(points[len(points)-1])
        Nslopes.append(slopes[len(slopes)-1])

        # Plot original Waypoints
        plot.figure(1)
        plot.xlim(0.33, 0.78)
        plot.ylim(-3.7,-0.3)
        plot.plot([p[0] for p in points], [p[1] for p in points], 'o')
        plot.title('All 992 Waypoints')

        # Plot N waypoints and a path using Cubic Hermite Spline curve fitting Method
        plot.figure(2)
        plot.xlim(0.33, 0.78)
        plot.ylim(-3.7,-0.3)
        plot.plot([p[0] for p in Npoints], [p[1] for p in Npoints], 'o')
        plot.title('Path using Cubic Hermite Spline curve fitting Method for N waypoints')
        M=np.array([[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]])
        
        for i in range(N+1):
            weigh=float(N*0.5)
            G1=np.array([[Npoints[i][1]],[Npoints[i+1][1]],[float(Nslopes[i][1]/weigh)],[float(Nslopes[i+1][1]/weigh)]])
            G2=np.array([[Npoints[i][0]],[Npoints[i+1][0]],[float(Nslopes[i][0]/weigh)],[float(Nslopes[i+1][0]/weigh)]])
    
            # Polynomial Coefficients
            V1=np.matmul(M,G1)
            V2=np.matmul(M,G2)
    
            X=[]
            Y=[]
            # Plot  New Path
            for u in np.arange(0, 1, 0.002):
                # Parametric equation for y
                y= (V1[0][0]*u**3)+(V1[1][0]*u**2)+(V1[2][0]*u)+V1[3][0]
                Y.append(y)
                # Parametric equation for x
                x= (V2[0][0]*u**3)+(V2[1][0]*u**2)+(V2[2][0]*u)+V2[3][0]
                X.append(x)
            plot.plot(X,Y)
        plot.show()

# function to listen to ros topic
def listener():
    print("Waiting for rosbag to finish playing...")
    rospy.init_node('waypoint_reducer', anonymous=True)
    rospy.Subscriber("/vslam2d_pose", PoseStamped, callback)
    rospy.spin()
 
        

if __name__ == '__main__':
    listener()
