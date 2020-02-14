import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
from drawnow import *
import transforms3d 

imus = serial.Serial('/dev/ttyACM0', 115200)
column_names = ["qw", "qx", "qy", "qz"]
wrist = pd.DataFrame(columns = column_names)
elbow = pd.DataFrame(columns = column_names)

cnt = 0

fig = plt.figure()
ax = plt.axes()
plt.ion()

shoulder = [0, 0, 2]
updated_point = [0, 0, 0.5]
test = [0, 0, 0.5]



while True:
    data = imus.readline().decode('ascii').replace('\r\n', '')#.replace('\t\tCALIBRATION', '').replace(':', '').replace('\t\t', '')
    data = data.split(',')
    print(data)
    if data[0] == 'Elbow':
        elbow = elbow.append({'qw':float(data[1]), 'qx':float(data[2]), 'qy':float(data[3]), 'qz':float(data[4])}, ignore_index=True)    
    #else:
    #    wrist = wrist.append({'qw':float(data[1]), 'qx':float(data[2]), 'qy':float(data[3]), 'qz':float(data[4])}, ignore_index=True)

    #elbow_q = elbow.loc[cnt]
    #wrist_q = wrist.loc[cnt]

    #print(elbow)#, wrist_q)

    cnt = cnt+1