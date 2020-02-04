import numpy as np
import pandas as pd
import serial  
import math
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
from drawnow import *
import transforms3d 

# -------------------------------
# Normalize the quaternion data before sending it !!?? --> Done in Arduino Code
# -------------------------------

imu = serial.Serial('/dev/ttyACM0', 115200)
column_names = ["qw", "qx", "qy", "qz"]
quaternions = pd.DataFrame(columns = column_names)

cnt = 0

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return [w, x, y, z]

def q_conjugate(q):
    w, x, y, z = q
    return [w, -x, -y, -z]

def qv_mult(q1, v1):
    q2 = [0.0, v1[0], v1[1], v1[2]]
    return q_mult(q_mult(q1, q2), q_conjugate(q1))


fig = plt.figure()
#fig.set_size_inches(10,10)
ax = fig.add_axes([0,0,1,1], projection='3d')
ax.set_xlim3d(0,3)
ax.set_ylim3d(0,3)
ax.set_zlim3d(0,3)
# set up lines and points
#lines = ax.plot([0,0], [0,0], [0,1], marker = '.')
#lines = ax.plot([0,0],[0,0],[1,2], marker = '.')
test_shoulder = [1.5, 1.5, 2]
test_point = [1.5, 1.5, 1]
test_q = [0, 1, 1, 1]
test_new = transforms3d.quaternions.rotate_vector(test_point, test_q)
lines = ax.plot([1.5,1.5], [1.5,1.5], [2,1], marker = '.')
lines = ax.plot([1.5,test_new[0]], [1.5,test_new[1]], [2,test_new[2]], marker = '.')
# Adds new line to plot line = plt3d.art3d.Line3D([0.5,0.5], [0.5,0.5], [1,0])
#ax.add_line(line)
plt.show()


fig = plt.figure()
ax = plt.axes(projection='3d', aspect = 'auto', autoscale_on = True)
plt.ion()

shoulder = [0, 0, 2]
updated_point = [0, 0, 1]
test = [0, 0, 0]
# Calculate the rotation matrix based on the updated vector ??
# Remove the infinte lines

def makeFig():
    #ax.plot([1.5,cnt], [1.5,cnt], [2,cnt])
    lines = ax.plot([0,test[0]], [0,test[1]], [2,test[2]], '-b', color = 'blue')
    #ax.plot(updated_point[0], updated_point[1], updated_point[2])
    #ax.plot(updated_point, [1.5, 1.5, 2])

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\tCALIBRATION', '').replace(':', '').replace('\t\t', '')
    x = data.split(' ')
    #print(x)
    if x[0] == 'qW':
        quaternions = quaternions.append({'qw':float(x[1]), 'qx':float(x[3]), 'qy':float(x[5]), 'qz':float(x[7])}, ignore_index=True)
        q = quaternions.loc[cnt]
        q_conj = [q[0], -q[1], -q[2], -q[3]]
        #print(q)
        print(np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2))   # Magnitude
        #M = transforms3d.quaternions.quat2mat(quaternions.loc[cnt])
        # - Addition method -- not sure how it works
        #temp = [(2*q[1]*q[3]-2*q[2]*q[0]), (2*q[2]*q[3]+2*q[1]*q[0]), (1-2*q[1]**2-2*q[2]**2)]
        #updated_point = temp + updated_point
        # -----
        # --- Multiplication method --> q * v * q'
        #qv = qv_mult(q, updated_point)
        #updated_point = qv_mult(qv, q_conj)

        #-----WORKS WELL ???? with always computing on the same point(elbow)-----#
        test = transforms3d.quaternions.rotate_vector(updated_point, q)

        print(test)
        makeFig() 
        plt.pause(0.0001)

        cnt += 1

        if np.mod(cnt, 100) == 0:
            plt.cla()
