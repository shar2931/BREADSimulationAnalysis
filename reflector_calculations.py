import numpy as np
import matplotlib.pyplot as plt

x1 = 15
f = 201 * 2
z = np.arange(-20.0, 20.5, 0.5)

y1 = np.sqrt(4 * f * x1)
phi1 = np.arctan(x1 / (z + y1))
phi2 = np.arctan((f / 2) / (z + 567.1))

zm = (((f / 2) - 15) * z - (f / 2) * 55.3) / 385
#alpha = np.arctan(2 * (zm - z) / f)
phiMax = np.arctan((f / 2) / (z - zm))

#print(phi1 * 180 / np.pi)
#print(phi2 * 180 / np.pi)
#print(phiMax * 180 / np.pi)
#print(np.abs(phi1 - phi2) / phiMax)

c = 40
R = 40
r = 20

#print(567.1 - 411.8)
#print(z - ((c - z) * (x1 + r) / (R - r)))
#print(z - ((c - z) * ((f/2) + r) / (R - r)))

for z_i in z:
    rPrime1 = np.arange(-1 * R, -1 * r, 0.01)
    rPrime2 = np.arange(-1 * r + 0.01, 0.01, 0.01)

    phiBottom1 = np.arctan((c - z_i) / (rPrime1 + r))
    phiTop1 = np.arctan((c - z_i - 20) / (rPrime1 - r))

    phiBottom2 = np.arctan((c - z_i - 20) / (rPrime2 + r))
    phiTop2 = np.arctan((c - z_i - 20) / (rPrime2 - r))
    print(phiBottom2 * 180 / np.pi)
    print(phiTop2 * 180 / np.pi)

    angles1 = np.abs(phiTop1 - phiBottom1) * 180 / np.pi
    angles2 = np.abs(phiTop2 - phiBottom2) * 180 / np.pi
    #print(np.sum(angles1) + np.sum(angles2))
