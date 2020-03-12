import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

data = pd.read_csv(r'rf_test.csv')

e_x = data['e_x']
e_y = data.iloc[:,1]
e_z = data.iloc[:,2]#['e_z']
w_x = data.iloc[:,3]#['w_x']
w_y = data.iloc[:,4]#['w_y']
w_z = data.iloc[:,5]#['w_z']


plt.plot(e_x)
plt.plot(e_y)
plt.plot(e_z)
plt.plot(w_x)
plt.plot(w_y)
plt.plot(w_z)

plt.show()