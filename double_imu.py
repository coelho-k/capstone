import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
import transforms3d 
import time, csv

# Make Serial Port a Parameter
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

result_file = open("rf_test.csv",'w')
wr = csv.writer(result_file)

shoulder = np.array([0, 0, 2])
updated_elbow = np.array([0, 0, 1.5])
elbow_seg = np.array([0, 0, 1.5])
updated_wrist = np.array([0, 0, 1.5])
wrist_seg = np.array([0, 0, 1.5])
axis_change = np.array([0.7071, 0, -0.7071, 0])


time.sleep(2)

global wrist_q# = [0,0,0,0]
global elbow_q# = [0,0,0,0]

while True:
    try:
        data = imus.readline().decode('ascii').replace('\r\n', '').replace(',', '').replace(':', '').replace('\t\t', '')
        data = data.split(' ')
        print(data)
    except:
        continue
    
    if len(data) == 11 and float(data[3]) == 0:
        wrist = wrist.append({'qw':float(data[7]), 'qx':float(data[8]), 'qy':float(data[9]), 'qz':float(data[10])}, ignore_index=True)
        wrist_q = wrist.loc[wrist_cnt]
        wrist_cnt += 1

    elif len(data) == 11 and float(data[3]) == 1:
        elbow = elbow.append({'qw':float(data[7]), 'qx':float(data[8]), 'qy':float(data[9]), 'qz':float(data[10])}, ignore_index=True)   
        elbow_q = elbow.loc[elbow_cnt]
        elbow_cnt += 1

    if (elbow_cnt >= 1 and wrist_cnt >= 1) and (wrist_cnt == elbow_cnt): 
        print('Elbow = ', elbow_q)
        print('Elbow Count = ', elbow_cnt)
        print('Wrist = ', wrist_q)
        print('Wrist Count = ', wrist_cnt)

        elbow_q = [elbow_q[0], -elbow_q[3], elbow_q[2], elbow_q[1]]
        wrist_q = [wrist_q[0], -wrist_q[3], wrist_q[2], wrist_q[1]]

        # ----------------- Implementing elbow rotation about a fixed point (shoulder) ---------------------
        temp = updated_elbow - shoulder
        elbow_seg = transforms3d.quaternions.rotate_vector(temp, elbow_q)
        elbow_seg = shoulder + elbow_seg
        # -------------------------------------------------------------------------------------------------#
        # -------------------- Aligning elbow IMU axes with shoulder ----------------------------------------#
        temp = elbow_seg - shoulder
        elbow_seg = transforms3d.quaternions.rotate_vector(temp, axis_change)
        elbow_seg = shoulder + elbow_seg
        #print('New Elbow Co-ordinates = ', elbow_seg)

        # ----------------- Implementing wrist rotation about elbow ---------------------
        temp = updated_wrist - shoulder
        wrist_seg = transforms3d.quaternions.rotate_vector(temp, wrist_q)
        wrist_seg = shoulder + wrist_seg 
        # -------------------------------------------------------------------------------------------------#
        # -------------------- Aligning wrist IMU axes with shoulder ----------------------------------------#
        temp = wrist_seg - shoulder
        wrist_seg = transforms3d.quaternions.rotate_vector(temp, axis_change)
        wrist_seg = shoulder + wrist_seg
        #print('New Wrist Co-ordinates = ', wrist_seg)

        # Only Translating the X and Y components of the wrist. Test more !!!!
        wrist_seg = [wrist_seg[0] + elbow_seg[0], wrist_seg[1] + elbow_seg[1], wrist_seg[2]]
        #joint_angle = np.sqrt(np.dot(np.dot(elbow_q[0] - wrist_q[1], elbow_q[1] - wrist_q[2]), np.dot(elbow_q[2] - wrist_q[3], elbow_q[3])))  # Fill it in
        #joint_angle = joint_angle * 360 # Unsure what this number should be
        #print ('Joint Angle = ', joint_angle)
        elbow_seg_list = list(elbow_seg)
        csv_row = elbow_seg_list + wrist_seg
        wr.writerow([wrist_q])
        
        
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
        