import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
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


"""fig = plt.figure()
ax = fig.add_axes([0,0,1,1], projection='3d')
ax.set_xlim3d(0,3)
ax.set_ylim3d(0,3)
ax.set_zlim3d(0,3)


test_shoulder = [1.5, 1.5, 2]
test_point = [1.5, 1.5, 1]
test_q = [0, 1, 1, 1]
test_new = transforms3d.quaternions.rotate_vector(test_point, test_q)
lines = ax.plot([1.5,1.5], [1.5,1.5], [2,1], marker = '.')
lines = ax.plot([1.5,test_new[0]], [1.5,test_new[1]], [2,test_new[2]], marker = '.')

plt.show()"""


fig = plt.figure()
ax = plt.axes(projection='3d', aspect = 'auto', autoscale_on = True)
plt.ion()

shoulder = [0, 0, 2]
updated_point = [0, 0, 1]
test = [0, 0, 1]
# Calculate the rotation matrix based on the updated vector ??
# Remove the infinte lines

def makeFig():
    #ax.plot([1.5,cnt], [1.5,cnt], [2,cnt])
    #lines = ax.plot([0,test[0]], [0,test[1]], [2,test[2]], marker = '.', color = 'blue')
    ax.scatter([0,test[0]], [0,test[1]], [0,test[2]], color = 'blue')
    #ax.plot(updated_point, [1.5, 1.5, 2])

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\tCALIBRATION', '').replace(':', '').replace('\t\t', '')
    x = data.split(' ')
    #print(x)
    if x[0] == 'qW':
        quaternions = quaternions.append({'qw':float(x[1]), 'qx':float(x[3]), 'qy':float(x[5]), 'qz':float(x[7])}, ignore_index=True)
        q = quaternions.loc[cnt]
        q_conj = [q[0], -q[1], -q[2], -q[3]]
        print(q)
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
        #------------------------------------------------------------------------
        #test = np.matmul(np.matmul(q, test), q_conj)


        print(test)
        makeFig() 
        plt.pause(0.0001)

        cnt += 1

        #if np.mod(cnt, 100) == 0:
        #    plt.cla()
