import pandas
import matplotlib.pyplot as plt
import numpy as np
#small max tries = 4 ; big = 4
df = pandas.DataFrame(dict(graph =['PPal', 'VDH', 'Brew', 'Gdruid', 'PWar'],
                           small =[60,     39,       87,       29,       47],
                           small2=[61,     35,       145,      32,       40],
                           small3=[61,     41,       162,      32,       42],
                           small4=[0,      35,       88,       31,        0],
                           big   =[38,     25,       57,       22,       38],
                           big2  =[40,     25,       52,       23,       36],
                           big3  =[41,     24,       49,       21,       36],
                           big4  =[0,       0,       56,       0,         0])) 

ind = np.arange(len(df))
width = 0.1

fig, ax = plt.subplots()
ax.barh(ind, 200, 0.02, color = 'black')
ax.barh(ind + 1*width, df.big, width, color='red', label='2500 DPS')
ax.barh(ind + 2*width, df.big2, width, color='darkred', label='2500 DPS')
ax.barh(ind + 3*width, df.big3, width, color='orangered', label='2500 DPS')
ax.barh(ind + 4*width, df.big4, width, color='lightcoral', label='2500 DPS')
ax.barh(ind + 5*width, df.small, width, color='green', label='2000 DPS')
ax.barh(ind + 6*width, df.small2, width, color='limegreen', label='2000 DPS')
ax.barh(ind + 7*width, df.small3, width, color='springgreen', label='2000 DPS')
ax.barh(ind + 8*width, df.small4, width, color='lawngreen', label='2000 DPS')


ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[8*width -1, len(df)])
ax.legend()
plt.savefig("TankDummyTests1.jpg")
plt.show()