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

        # Normalize  --> Divide each component by the magnitude
        # Trying to keep the segment as 0.2 magnitude

        #test_mag = np.sqrt(test[0]**2 + test[1]**2 + (test[2] - 0.5)**2)
        #print('Test mag = ', test_mag)
        #test = [test[0] / test_mag, test[1] / test_mag, test[2] / test_mag]
# -------------------------------

imu = serial.Serial('/dev/ttyACM0', 115200)
column_names = ["qw", "qx", "qy", "qz"]
quaternions = pd.DataFrame(columns = column_names)

cnt = 0

fig = plt.figure()
ax = plt.axes(projection='3d')
###ax = plt.axes()
plt.ion()



# SCALE BASED ON HEIGHT INPUT --> TO DO
shoulder = np.array([0, 0, 2])
updated_point = np.array([0, 0, 1])
test = np.array([0, 0, 1])
axis_change = np.array([0.7071, 0, 0.7071, 0])
#q_rest = [0.3839, -0.4862, 0.4019, 0.6743] --> For trying to create a reference rotation

"""
def makeFig():
    #ax.plot([1.5,cnt], [1.5,cnt], [2,cnt])
    #lines = ax.plot([0,test[0]], [0,test[1]], [2,test[2]], marker = '.', color = 'blue')
    ax.plot([0,test[0]], [0,test[1]], [2,test[2]], color = 'blue')
    #ax.plot(updated_point, [1.5, 1.5, 2])
"""

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\tCALIBRATION', '').replace(':', '').replace('\t\t', '')
    x = data.split(' ')
    print(x)
    #if float(x[8].replace('Sys=', '')) == 0:
    #    continue
    if x[0] == 'qW':
        quaternions = quaternions.append({'qw':float(x[1]), 'qx':float(x[3]), 'qy':float(x[5]), 'qz':float(x[7])}, ignore_index=True)
        q = quaternions.loc[cnt]

        # ------------------- Print Checks ----------------------------------
        print(q)
        print(np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2))   
        # -------------------------------------------------------------------

        # ----------------- Implementing the rotation about a fixed point (shoulder) ---------------------
        temp = updated_point - shoulder
        test = transforms3d.quaternions.rotate_vector(temp, q)
        test = shoulder + test
        # -------------------------------------------------------------------------------------------------#
        # -------------------- Aligning the IMU axes with shoulder ----------------------------------------#
        temp = test - shoulder
        test = transforms3d.quaternions.rotate_vector(temp, axis_change)
        test = shoulder + test
        print('New Co-ordinates = ', test)
        # -------------------------------------------------------------------------------------------------#

        # makeFig()
        ax.plot([0, 0], [0, 0], [2, 1], color = 'blue', marker = '.')   # TORSE
        ax.plot([0, 0.2], [0, 0.2], [1, 0], color = 'blue', marker = '.')   # LEG
        ax.plot([0, -0.2], [0, -0.2], [1, 0], color = 'blue', marker = '.') # LEG 
        ax.plot([shoulder[0], test[0]], [shoulder[1], test[1]], [shoulder[2], test[2]], color = 'blue', marker = '.')   # ARM SEGMENT
        plt.autoscale(False)
        plt.xlim(-2,2)
        plt.ylim(-2,2)
        ax.set_zlim(0, 2)
        plt.xlabel('x')
        plt.ylabel('y')
        
        plt.pause(0.0001)
        ax.cla()
        cnt += 1

        #if np.mod(cnt, 100) == 0:
        #    plt.cla()
