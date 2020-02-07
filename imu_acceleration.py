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

velocity_x = [0]
velocity_y = [0]
velocity_z = [0]

position_x = [0]
position_y = [0]
position_z = [0]


cnt = 0


#fig = plt.figure()
#ax = plt.axes(projection='3d', aspect = 'auto', autoscale_on = True)
plt.ion()
plt.legend()


def makeFig():
    plt.plot(position_x, 'bo-')
    plt.plot(position_y, 'go-')
    plt.plot(position_z, 'ro-')

while True:
    data = imu.readline().decode('ascii').replace('\r\n', '').replace('\t\t', '').replace(':', '').replace('\t\t', '')
    x = data.split(' ')
    #print(x)
    if x[0] == 'linear':
        a_x.append(float(x[2]))
        a_y.append(float(x[4]))
        a_z.append(float(x[6]))
        #print(a)

        if cnt >= 1:
            # First integration
            velocity_x.append(velocity_x[cnt-1]  +  a_x[cnt-1]  +  ((a_x[cnt]  -  a_x[cnt-1]) > 1)) 
            velocity_y.append(velocity_y[cnt-1]  +  a_y[cnt-1]  +  ((a_y[cnt]  -  a_y[cnt-1]) > 1)) 
            velocity_z.append(velocity_z[cnt-1]  +  a_z[cnt-1]  +  ((a_z[cnt]  -  a_z[cnt-1]) > 1)) 
            print(velocity_x[cnt], velocity_y[cnt], velocity_z[cnt])

            # Second integration
            position_x.append(position_x[cnt-1] + velocity_x[cnt-1] + ((velocity_x[cnt] - velocity_x[cnt-1]) > 1))
            position_y.append(position_y[cnt-1] + velocity_y[cnt-1] + ((velocity_y[cnt] - velocity_y[cnt-1]) > 1))
            position_z.append(position_z[cnt-1] + velocity_z[cnt-1] + ((velocity_z[cnt] - velocity_z[cnt-1]) > 1))

        drawnow(makeFig) 
        plt.pause(0.000001)

        cnt += 1

        #if np.mod(cnt, 100) == 0:
        #    plt.cla()
