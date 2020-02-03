import numpy as np
import pandas as pd
import serial  
import math
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
from matplotlib import animation
from scipy.spatial.transform import Rotation as R
from drawnow import *
import transforms3d 

# -------------------------------
# Normalize the quaternion data before sending it !!??
# -------------------------------

imu = serial.Serial('COM6', 115200)
column_names = ["qw", "qx", "qy", "qz"]
quaternions = pd.DataFrame(columns = column_names)

cnt = 0

def quaternion_matrix(quaternion):
    """Return homogeneous rotation matrix from quaternion.

    >>> M = quaternion_matrix([0.99810947, 0.06146124, 0, 0])
    https://www.lfd.uci.edu/~gohlke/code/transformations.py.html

    """
    q = np.array(quaternion, dtype=np.float64, copy=True)
    n = np.dot(q, q)
    #if n < _EPS:
    #    return np.identity(4)
    q *= math.sqrt(2.0 / n)
    q = np.outer(q, q)
    return np.array([
        [1.0 - q[2, 2] - q[3, 3], q[1, 2] - q[3, 0], q[1, 3] + q[2, 0]],
        [q[1, 2] + q[3, 0], 1.0 - q[1, 1] - q[3, 3], q[2, 3] - q[1, 0]],
        [q[1, 3] - q[2, 0], q[2, 3] + q[1, 0], 1.0 - q[1, 1] - q[2, 2]]
        ])


fig = plt.figure()
fig.set_size_inches(10,10)
ax = fig.add_axes([0,0,1,1], projection='3d')
# set up lines and points
#lines = ax.plot([0,0], [0,0], [0,1], marker = '.')
#lines = ax.plot([0,0],[0,0],[1,2], marker = '.')
lines = ax.plot([0.5,0.5], [0.5,0.5], [1,0], marker = '.')
# Adds new line to plot line = plt3d.art3d.Line3D([0.5,0.5], [0.5,0.5], [1,0])
#ax.add_line(line)
plt.show()


fig = plt.figure()
fig.set_size_inches(10,10)
ax = fig.add_subplot(111, projection='3d')
plt.ion()

shoulder = [1.5, 1.5, 2]
updated_point = [1.5, 1.5, 1]
# Calculate the rotation matrix based on the updated vector
# Remove the infinte lines

def makeFig():
    #ax.plot([1.5,cnt], [1.5,cnt], [2,cnt])
    line = ax.plot([1.5,updated_point[0]], [1.5,updated_point[1]], [2,updated_point[2]], marker = '.', color = 'red')
    #ax.plot(updated_point[0], updated_point[1], updated_point[2])
    #ax.plot(updated_point, [1.5, 1.5, 2])

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\tCALIBRATION', '').replace(':', '')
    x = data.split(' ')
    #print(x)
    if x[0] == 'qW':
        quaternions = quaternions.append({'qw':float(x[1]), 'qx':float(x[3]), 'qy':float(x[5]), 'qz':float(x[7])}, ignore_index=True)
        q = quaternions.loc[cnt]
        print(q)
        #M = transforms3d.quaternions.quat2mat(quaternions.loc[cnt])
        temp = [(2*q[1]*q[3]-2*q[2]*q[0]), (2*q[2]*q[3]+2*q[1]*q[0]), (1-2*q[1]**2-2*q[2]**2)]
        updated_point = temp + updated_point
        print(updated_point)
        makeFig() 
        plt.pause(0.0001)

        cnt += 1
