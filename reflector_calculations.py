import numpy as np

x1 = 15
f = 201 * 2
z = np.arange(-10.0, 10.0, 0.5)

y1 = np.sqrt(4 * f * x1)
phi1 = np.arctan((y1 ** 2) / ((y1 - z) * 4 * f))

phi2 = np.arctan(f / (2 * (f * np.sqrt(2) - z)))

y2 = ((f - 2 * x1) * z + f * y1) / (2 * f - 2 * x1)
alpha = np.arctan(2 * (y2 - z) / f)
phiMax = (np.pi / 2) - alpha

print(phi1)
print(np.abs(phi1 - phi2) / phiMax)
