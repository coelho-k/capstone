import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
import transforms3d 

data = pd.read_csv(r'all_in_one_26_2_20.csv')
x = data['x']
y = data['y']
z = data['z']
mag = []

for ii in range(len(x)):
    mag.append(np.sqrt(x[ii]**2 + y[ii]**2 + z[ii]**2))

plt.plot(z, label = 'z')
plt.plot(y, label = 'y')
plt.plot(x, label = 'x')
plt.plot(mag, label = 'mag')
plt.legend()
plt.show()

plt.plot(x[950:], y[950:])
plt.show()