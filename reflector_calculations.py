import numpy as np
import matplotlib.pyplot as plt

x1 = 15
f = 201 * 2
z = np.arange(-20.0, 20.5, 0.5)

y1 = np.sqrt(4 * f * x1)
phi1 = np.arctan(x1 / (z + y1))
phi2 = np.arctan((f / 2) / (z + 567.1))

zm = (((f / 2) - 15) * z - (f / 2) * 55.3) / 387
#alpha = np.arctan(2 * (zm - z) / f)
phiMax = np.arctan((f / 2) / (z - zm))

#print(phi1 * 180 / np.pi)
#print((phi2 - phi1) * 180 / np.pi)
#print(phiMax * 180 / np.pi)
#reflAngleProp = np.abs(phi1 - phi2) / (phiMax - phi1)

plt.scatter(z, (phi2 - phi1) * 180 / np.pi)
plt.savefig('image.png')

c = 40
t = 20
R = np.array([40, 60])
r = np.array([15, 20, 30])

combs = np.array(np.meshgrid(R, r)).T.reshape(6, 2)
alpha = np.divide(combs[:, 0], combs[:, 0] + combs[:, 1])
z0 = (c - alpha * (c - t)) / (1 + alpha)
theta = np.arctan((c - z0) / combs[:, 0])
print(z0 * theta / (np.pi / 2))
