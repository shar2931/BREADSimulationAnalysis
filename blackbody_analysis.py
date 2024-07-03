import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description = 'Normalized Option')
parser.add_argument('--norm', type = bool, default = False)
args = parser.parse_args()
normalized = parser.norm

numFiles = 20
fpath = 'BlackbodyStudiesData/2024-07-02/'
fname = 'SNSPD-'

plotDataXS = {}
plotDataS = {}
plotDataM = {}
plotDataL = {}

for findex in range(numFiles):  
    with open(fpath + fname + str(findex) + '.dat') as f:
        line = f.readline()
        while 'BeginData' not in line:
            if 'ORIGIN_POSITION' in line:
                splitLine = line.strip().split(' ')
                originPos = (float(splitLine[1]) * 200, float(splitLine[2]) * 200, float(splitLine[3]) * 200)

            elif 'A_AXIS_DIM' in line:
                line.strip().split(' ')
                xBins = line[1]

            elif 'B_AXIS_DIM' in line:
                line.strip().split(' ')
                yBins = line[1]

            line = f.readline()

        line = f.readline()
        dataArray = np.array(line.strip().split(' '))
        line = f.readline()
        while line.strip().split(' ') != ['']:
            dataArray = np.vstack((dataArray, np.array(line.strip().split(' '))))
            line = f.readline()

        dataArray = dataArray.astype(float)
        plotDataXS[originPos] = np.sum(dataArray[10, 10])
        plotDataS[originPos] = np.sum(dataArray[8:13, 8:13])
        plotDataM[originPos] = np.sum(dataArray[6:15, 6:15])
        plotDataL[originPos] = np.sum(dataArray[:, :])

planeXS = list(plotDataXS.keys())
irradXS = {pos[2]: plotDataXS[pos] for pos in planeXS}
sortedXS = sorted(irradXS.items())    
zXS, fXS = zip(*sortedXS)

nRaysXS = [irrad * 10**8 * (0.03333/21)**2 for irrad in fXS]
errXS = np.sqrt(nRaysXS) * 10**-8 / ((0.03333 / 21) ** 2)

errXS = np.sqrt(np.square(np.divide(errXS, fXS[10])), np.square(np.divide(np.multiply(errXS[10], errXS), fXS[10]**2)))
fXS = np.multiply(fXS, 1 / fXS[10])
#plt.errorbar(zXS, fXS, yerr = errXS, fmt = 'o', label = '0.63mm x 0.63mm')

planeS = list(plotDataS.keys())
irradS = {pos[2]: plotDataS[pos] for pos in planeS}
sortedS = sorted(irradS.items())    
zS, fS = zip(*sortedS)

nRaysS = [irrad * 10**8 * (0.03333/21)**2 for irrad in fS]
errS = np.sqrt(nRaysS) * 10**-8 / ((0.03333 / 21) ** 2)

errS = np.sqrt(np.square(np.divide(errS, fS[10])), np.square(np.divide(np.multiply(errS[10], errS), fS[10]**2)))
fS = np.multiply(fS, 1 / fS[10])
plt.errorbar(zS, fS, yerr = errS, fmt = 'o', label = '1.9mm x 1.9mm')

planeM = list(plotDataM.keys())
irradM = {pos[2]: plotDataM[pos] for pos in planeM}
sortedM = sorted(irradM.items())    
zM, fM = zip(*sortedM)

nRaysM = [irrad * 10**8 * (0.03333/21)**2 for irrad in fM]
errM = np.sqrt(nRaysM) * 10**-8 / ((0.03333 / 21) ** 2)

errM = np.sqrt(np.square(np.divide(errM, fM[10])), np.square(np.divide(np.multiply(errM[10], errM), fM[10]**2)))
fM = np.multiply(fM, 1 / fM[10])
plt.errorbar(zM, fM, yerr = errM, fmt = 'o', label = '3.2mm x 3.2mm')

planeL = list(plotDataL.keys())
irradL = {pos[2]: plotDataL[pos] for pos in planeL}
sortedL = sorted(irradL.items())    
zL, fL = zip(*sortedL)

nRaysL = [irrad * 10**8 * (0.03333/21)**2 for irrad in fL]
errL = np.sqrt(nRaysL) * 10**-8 / ((0.03333 / 21) ** 2)

errL = np.sqrt(np.square(np.divide(errL, fL[10])), np.square(np.divide(np.multiply(errL[10], errL), fL[10]**2)))
fL = np.multiply(fL, 1 / fL[10])
plt.errorbar(zL, fL, yerr = errL, fmt = 'o', label = '13.3mm x 13.3mm')

plt.title('Normalized Power for Various Detector Sizes Along z-axis')
plt.xlabel('z Shift from Focus (mm)')
plt.ylabel('Normalized Power')
plt.xticks(np.arange(-20, 20, step=4))
plt.legend()
plt.savefig('z-axis-irradiance-normalized.png')
