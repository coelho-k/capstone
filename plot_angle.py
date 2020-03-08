import numpy as np
import pandas as pd
import serial  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d
import transforms3d 

data = pd.read_csv(r'angle_test.csv')
data.fillna(0)

plt.plot(data)
plt.show()