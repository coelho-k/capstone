import matplotlib.pyplot as plot 
import numpy as np 
import pandas as pd 

data = pd.read_csv(r'up_down.csv')

#plt.plot(data.loc[:, '1.5332010933747549'] - np.mean(data.loc[:, '1.5332010933747549']))
#plt.show()

time        = np.arange(0, 10, 0.1)

 

# Amplitude of the sine wave is sine of a variable like time

amplitude   = np.sin(time)

 

# Plot a sine wave using time and amplitude obtained for the sine wave

plot.plot(time, amplitude)

 

# Give a title for the sine wave plot

plot.title('Sine wave')

 

# Give x axis label for the sine wave plot

plot.xlabel('Time')

 

# Give y axis label for the sine wave plot

plot.ylabel('Amplitude = sin(time)')

 

plot.grid(True, which='both')

 

plot.axhline(y=0, color='k')

plot.hlines(0.5, 0, 10, color = 'red')
plot.hlines(-0.5, 0, 10, color= 'red')

plot.plot(time, amplitude * np.exp(-time * 0.5))

plot.show()

 

# Display the sine wave

plot.show()