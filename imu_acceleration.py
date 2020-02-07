import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
from drawnow import *
import transforms3d 


imu = serial.Serial('/dev/ttyACM0', 115200)
a_x = []
a_y = []
a_z = []

cnt = 0


#fig = plt.figure()
#ax = plt.axes(projection='3d', aspect = 'auto', autoscale_on = True)
plt.ion()
plt.legend()


def makeFig():
    plt.plot(a_x, 'bo-')
    plt.plot(a_y, 'go-')
    plt.plot(a_z, 'ro-')

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\t', '').replace(':', '').replace('\t\t', '')
    x = data.split(' ')
    #print(x)
    if x[0] == 'linear':
        a_x.append(float(x[2]))
        a_y.append(float(x[4]))
        a_z.append(float(x[6]))
        #print(a)

        drawnow(makeFig) 
        plt.pause(0.000001)

        cnt += 1

        #if np.mod(cnt, 100) == 0:
        #    plt.cla()
