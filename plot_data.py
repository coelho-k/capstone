import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

data = pd.read_csv(r'abduction_25_2_20.csv')
mag = []

for ii in range(len(data.loc[:, 'x'])):
    mag.append(np.sqrt(data.loc[ii, 'x']**2 + data.loc[ii, 'y']**2 + data.loc[ii, 'z']**2))

#plt.plot(data.loc[:, 'x'] - np.mean(data.loc[:, 'y']))
#plt.show()

plt.plot(mag)
plt.show()