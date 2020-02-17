import transforms3d
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

fig = plt.figure()
ax = plt.axes(projection='3d')

shoulder = np.array([0,0,2])
elbow = np.array([0,0,1])


q = [0, 0.7071, 0, -0.7071]
v = elbow - shoulder
new_v = transforms3d.quaternions.rotate_vector(v, q)
new_v = shoulder + new_v

plt.plot([shoulder[0], v[0]], [shoulder[1], v[1]], [shoulder[2], v[2]], marker = '.')
plt.plot([shoulder[0], new_v[0]], [shoulder[1], new_v[1]], [shoulder[2], new_v[2]], marker = '.')

q = [0, 0.5, 0.5, -0.5]
v = elbow - shoulder
new_v = transforms3d.quaternions.rotate_vector(v, q)
new_v = shoulder + new_v
plt.plot([shoulder[0], new_v[0]], [shoulder[1], new_v[1]], [shoulder[2], new_v[2]], marker = '.')
plt.show()