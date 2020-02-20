import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
import transforms3d 
import time

imus = serial.Serial('/dev/ttyACM0', 115200)
column_names = ["qw", "qx", "qy", "qz"]
wrist = pd.DataFrame(columns = column_names)
elbow = pd.DataFrame(columns = column_names)

elbow_cnt = 0
wrist_cnt = 0

fig = plt.figure()
ax = plt.axes(projection='3d')
###ax = plt.axes()
plt.ion()

shoulder = np.array([0, 0, 2])
updated_elbow = np.array([0, 0, 1.5])
updated_wrist = np.array([0, 0, 1])
wrist_seg = np.array([0, 0, 1])
elbow_seg = np.array([0,0,1.5])
axis_change = np.array([0.7071, 0, 0.7071, 0])


time.sleep(2)

global wrist_q# = [0,0,0,0]
global elbow_q# = [0,0,0,0]

while True:
    try:
        data = imus.readline().decode('ascii').replace('\r\n', '')#.replace('\t\tCALIBRATION', '').replace(':', '').replace('\t\t', '')
        data = data.split(',')
        #print(data)
    except:
        continue
    
    if len(data) == 5 and float(data[4]) == 1.00: 
        wrist = wrist.append({'qw':float(data[0]), 'qx':float(data[1]), 'qy':float(data[2]), 'qz':float(data[3])}, ignore_index=True)
        wrist_q = wrist.loc[wrist_cnt]
        wrist_cnt += 1
    
    elif len(data) == 5 and float(data[4]) == 2.00:
        elbow = elbow.append({'qw':float(data[0]), 'qx':float(data[1]), 'qy':float(data[2]), 'qz':float(data[3])}, ignore_index=True)   
        elbow_q = elbow.loc[elbow_cnt]
        elbow_cnt += 1
    else:
        continue

    if elbow_cnt >= 1 and wrist_cnt >= 1: 
        print('Elbow = ', elbow_q, '\n')
        print('Wrist = ', wrist_q)

        """# ----------------- Implementing elbow rotation about a fixed point (shoulder) ---------------------
        temp = updated_elbow - shoulder
        elbow_seg = transforms3d.quaternions.rotate_vector(temp, elbow_q)
        elbow_seg = shoulder + elbow_seg
        # -------------------------------------------------------------------------------------------------#
        # -------------------- Aligning elbow IMU axes with shoulder ----------------------------------------#
        temp = elbow_seg - shoulder
        elbow_seg = transforms3d.quaternions.rotate_vector(temp, axis_change)
        elbow_seg = shoulder + elbow_seg
        print('New Co-ordinates = ', elbow_seg)"""

        # ----------------- Implementing wrist rotation about a fixed point (shoulder) ---------------------
        temp = updated_wrist - elbow_seg
        wrist_seg = transforms3d.quaternions.rotate_vector(temp, wrist_q)
        wrist_seg = elbow_seg + wrist_seg
        # -------------------------------------------------------------------------------------------------#
        # -------------------- Aligning wrist IMU axes with shoulder ----------------------------------------#
        temp = wrist_seg - elbow_seg
        wrist_seg = transforms3d.quaternions.rotate_vector(temp, axis_change)
        wrist_seg = elbow_seg + wrist_seg
        print('New Co-ordinates = ', wrist_seg)


        ax.plot([0, 0], [0, 0], [2, 1], color = 'blue', marker = '.')   # TORSE
        ax.plot([0, 0.2], [0, 0.2], [1, 0], color = 'blue', marker = '.')   # LEG
        ax.plot([0, -0.2], [0, -0.2], [1, 0], color = 'blue', marker = '.') # LEG 
        ax.plot([elbow_seg[0], wrist_seg[0]], [elbow_seg[1], wrist_seg[1]], [elbow_seg[2], wrist_seg[2]], color = 'blue', marker = '.')   # WRIST SEGMENT
        ax.plot([shoulder[0], elbow_seg[0]], [shoulder[1], elbow_seg[1]], [shoulder[2], elbow_seg[2]], color = 'blue', marker = '.')   # ARM SEGMENT
        plt.autoscale(False)
        plt.xlim(-2,2)
        plt.ylim(-2,2)
        ax.set_zlim(0, 3)
        plt.xlabel('x')
        plt.ylabel('y')
        
        plt.pause(0.0000001)
        ax.cla()
        
