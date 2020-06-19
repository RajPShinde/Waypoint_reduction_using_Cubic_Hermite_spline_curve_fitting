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
    euler = tf.transformations.euler_from_quaternion([0, 0, round(msg.pose.orientation.z,2), round(msg.pose.orientation.w,2)])
    points.append([msg.pose.position.x,msg.pose.position.y])
    slopes.append(math.tan(euler[2]))
    print(len(points))
    if len(points)>991: 
        draw_path(points)

      
# Draw the Paths
def draw_path(points):

    # Plot original Waypoints
    print(len(points))
    plot.subplot(211)
    plot.plot([p[0] for p in points], [p[1] for p in points], 'o')
    plot.show(block=False)
    
    while True:
        N=take_input()
        # Select N waypoints
        # Append the start point x,y and slope
        Npoints=[points[0]]
        Nslopes=[slopes[0]]
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
        print(len(Npoints)-2)

        # Plot N waypoints and a path using Cubic Hermite Spline curve fitting Method
        #Npoints.sort()
        plot.figure(1)
        plot.subplot(212)
        plot.plot([p[0] for p in Npoints], [p[1] for p in Npoints], 'o')
        M=np.array([[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]])
        for i in range(N+1):
            if Npoints[i+1][0]<Npoints[i][0]:
                xmin=Npoints[i+1][0]
                diff=abs(Npoints[i][0]-Npoints[i+1][0])
                G=np.array([[Npoints[i+1][1]],[Npoints[i][1]],[Nslopes[i+1]*diff],[Nslopes[i]*diff]])
            else:
                xmin=Npoints[i][0]
                diff=abs(Npoints[i+1][0]-Npoints[i][0])
                G=np.array([[Npoints[i][1]],[Npoints[i+1][1]],[Nslopes[i]*diff],[Nslopes[i+1]*diff]])
    
            # Polynomial Weights
            V=np.matmul(M,G)
            print(V)
    
            X=[]
            Y=[]
            # Plot  New Path
            for x in np.arange(0, 1, 0.002):
                y= (V[0][0]*x**3)+(V[1][0]*x**2)+(V[2][0]*x)+V[3][0]
                # Remap from 0-1 to x1-x2
                x=xmin+(diff*x)
                X.append(x)
                Y.append(y)
                plot.plot(X,Y)
        plot.show()

def listener():
    print("Waiting for rosbag to finish playing...")
    rospy.init_node('waypoint_reducer', anonymous=True)
    rospy.Subscriber("/vslam2d_pose", PoseStamped, callback)
    rospy.spin()
 
        

if __name__ == '__main__':
    listener()
