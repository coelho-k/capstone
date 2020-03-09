import transforms3d
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

fig = plt.figure()
ax = plt.axes(projection='3d')

shoulder = np.array([0, 0, 2])
updated_elbow = np.array([0, 0.5, 2])
elbow_seg = np.array([0, 0.5, 2])
updated_wrist = np.array([0, 0.5, 2.5])
wrist_seg = np.array([0, 0.5, 2.5])
axis_change = np.array([0.7071, 0, 0.7071, 0])


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

plt.show()