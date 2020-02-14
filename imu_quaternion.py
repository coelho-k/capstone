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

fig = plt.figure()
ax = plt.axes(projection='3d')
###ax = plt.axes()
plt.ion()



# SCALE BASED ON HEIGHT INPUT
shoulder = [0, 0, 2]
updated_point = [0, 0, 0.5]
test = [0, 0, 0.5]
q_rest = [0.3839, -0.4862, 0.4019, 0.6743]

def makeFig():
    #ax.plot([1.5,cnt], [1.5,cnt], [2,cnt])
    #lines = ax.plot([0,test[0]], [0,test[1]], [2,test[2]], marker = '.', color = 'blue')
    ax.plot([0,test[0]], [0,test[1]], [2,test[2]], color = 'blue')
    #ax.plot(updated_point, [1.5, 1.5, 2])

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\tCALIBRATION', '').replace(':', '').replace('\t\t', '')
    x = data.split(' ')
    print(x)
    #if float(x[8].replace('Sys=', '')) == 0:
    #    continue
    if x[0] == 'qW':
        quaternions = quaternions.append({'qw':float(x[1]), 'qx':float(x[3]), 'qy':float(x[5]), 'qz':float(x[7])}, ignore_index=True)
        q = quaternions.loc[cnt]
        temp = q[1]
        q[2] = -temp
        q[1] = q[2]
        #q_conj = [q[0], -q[1], -q[2], -q[3]]
        print(q)
        #q = transforms3d.quaternions.qmult(transforms3d.quaternions.qinverse(q_rest), q)

        print(np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2))   # Magnitude
        #M = transforms3d.quaternions.quat2mat(quaternions.loc[cnt])

        # --- Multiplication method --> q * v * q'

        #-----WORKS WELL ???? with always computing on the same point(elbow)-----#
        test = transforms3d.quaternions.rotate_vector(updated_point, q)
        #------------------------------------------------------------------------#
        # Normalize  --> Divide each component by the magnitude
        # Trying to keep the segment as 0.2 magnitude

        test_mag = np.sqrt(test[0]**2 + test[1]**2 + (test[2] - 0.5)**2)
        print('Test mag = ', test_mag)
        test = [test[0] / test_mag, test[1] / test_mag, test[2] / test_mag]

        print('New Co-ordinates = ', test)
        # makeFig()
        ax.plot([0, 0], [0, 0], [1, 0.5], color = 'blue', marker = '.') 
        ax.plot([0, 0.2], [0, 0.2], [0.5, 0], color = 'blue', marker = '.') 
        ax.plot([0, -0.2], [0, -0.2], [0.5, 0], color = 'blue', marker = '.') 
        ax.plot([0, test[0]], [0, test[1]], [0.75, test[2]], color = 'blue', marker = '.')
        #ax.plot([test[0], 0.2], [test[1], 0.2], [test[2], 0.2], color = 'blue', marker = '.')
        ###plt.plot(test[0], test[1], 'o', color = 'blue')
        plt.autoscale(False)
        plt.xlim(-1,1)
        plt.ylim(-1.1)
        ax.set_zlim(0, 2)
        plt.xlabel('x')
        plt.ylabel('y')
        
        plt.pause(0.0001)
        ax.cla()
        cnt += 1

        #if np.mod(cnt, 100) == 0:
        #    plt.cla()
