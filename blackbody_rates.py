import numpy as np
import matplotlib.pyplot as plt

# Physical Constants
k = 1.380649e-23 #J/K
h = 6.62607015e-34 #Js
c = 2.99794458e8 #m/s

absorberRadius = (0.6 * 200) / 1000
absorberArea = np.pi * (absorberRadius ** 2)

dLambda = 0.01
lamRange10 = np.arange(0.6, 10, dLambda) * 10**-6
lamRange15 = np.arange(0.6, 15, dLambda) * 10**-6
lamRange20 = np.arange(0.6, 20, dLambda) * 10**-6
lamRange25 = np.arange(0.6, 25, dLambda) * 10**-6
lamRange30 = np.arange(0.6, 30, dLambda) * 10**-6

TRange = np.arange(10, 45, 0.01)
integrationTime = 60 * 60

n_lam10 = {T : np.sum((8 * np.pi / np.power(lamRange10, 4)) / (np.exp((h * c) / (lamRange10 * k * T)) - 1)) * absorberArea * dLambda  for T in TRange}
n_lam15 = {T : np.sum((8 * np.pi / np.power(lamRange15, 4)) / (np.exp((h * c) / (lamRange15 * k * T)) - 1)) * absorberArea * dLambda  for T in TRange}
n_lam20 = {T : np.sum((8 * np.pi / np.power(lamRange20, 4)) / (np.exp((h * c) / (lamRange20 * k * T)) - 1)) * absorberArea * dLambda  for T in TRange}
n_lam25 = {T : np.sum((8 * np.pi / np.power(lamRange25, 4)) / (np.exp((h * c) / (lamRange25 * k * T)) - 1)) * absorberArea * dLambda  for T in TRange}
n_lam30 = {T : np.sum((8 * np.pi / np.power(lamRange30, 4)) / (np.exp((h * c) / (lamRange30 * k * T)) - 1)) * absorberArea * dLambda  for T in TRange}


sorted10 = sorted(n_lam10.items())   
T10, n10 = zip(*sorted10)

sorted15 = sorted(n_lam15.items())   
T15, n15 = zip(*sorted15)

sorted20 = sorted(n_lam20.items())   
T20, n20 = zip(*sorted20)

sorted25 = sorted(n_lam25.items())   
T25, n25 = zip(*sorted25)

sorted30 = sorted(n_lam30.items())   
T30, n30 = zip(*sorted30)

plt.plot(T10, n10, label = r'$\lambda \in [0.6, 10]$ $\mu m$')

plt.plot(T15, n15, label = r'$\lambda \in [0.6, 15]$ $\mu m$')

plt.plot(T20, n20, label = r'$\lambda \in [0.6, 20]$ $\mu m$')

plt.plot(T25, n25, label = r'$\lambda \in [0.6, 25]$ $\mu m$')

plt.plot(T30, n30, label = r'$\lambda \in [0.6, 30]$ $\mu m$')

plt.plot(T30, ((5 * (1.4e-6) / ((1.3e-6)**2)) * np.ones_like(n30)) / (1 * 60), label = r'N_B / $\tau = 1$min')

plt.plot(T30, ((5 * (1.4e-6) / ((1.3e-6)**2)) * np.ones_like(n30)) / (10 * 60), label = r'N_B / $\tau = 10$min')

plt.plot(T30, ((5 * (1.4e-6) / ((1.3e-6)**2)) * np.ones_like(n30)) / (60 * 60), label = r'N_B / $\tau = 60$min')

plt.xlabel('T (K)')
plt.ylabel('photons / sec')
plt.ylim(10**2, 10**5)
plt.title(r'Blackbody Photon Emission Rates for Various SNSPD $\lambda$ Ranges')
plt.yscale('log')
plt.legend()
plt.savefig('blackbody-rates-20um.png')
