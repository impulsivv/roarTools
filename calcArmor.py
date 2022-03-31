import matplotlib.pyplot as plt
import numpy as np

maxarmor = 300
x = np.linspace(0,maxarmor,50)
y = (0.01 * x) / (1+0.01 * x)

plt.xlabel("Armor")
plt.ylabel("Reduction in % ")

plt.grid(True)
plt.xticks([i for i in range(0,maxarmor, 20)])
plt.plot(x,y*100,'r')

plt.savefig('foo.png')
plt.show()