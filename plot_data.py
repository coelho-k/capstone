import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

data = pd.read_csv(r'up_down.csv')

plt.plot(data.loc[:, '1.5332010933747549'])
plt.show()