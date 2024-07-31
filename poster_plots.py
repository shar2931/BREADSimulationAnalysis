import numpy as np
import matplotlib.pyplot as plt
import argparse
import os


parser = argparse.ArgumentParser(description = 'FRED Data File Analyzer')
parser.add_argument('--norm', action = 'store_true')
args = parser.parse_args()
normalized = args.norm

numFiles = 8
fpath = 'BlackbodyStudiesData/2024-07-'
fpaths = [fpath + '02/', fpath + '03/', fpath + '05/', fpath + '07/', fpath + '15/']
#fpaths.remove(fpath + '15/')
fname = 'SNSPD-'

labels = {fpath + '02/': '40mm source, 20mm mount', fpath + '03/': '40mm source, 30mm mount', fpath + '05/': '60mm source, 20mm mount', fpath + '07/': '60mm source, 30mm mount', fpath + '15/': '80mm source, 14mm mount'}

plotDataXS = {}
plotDataS = {}
plotDataM = {}
plotDataL = {}

for fpath in fpaths:
    plotDataL = {}
    numFiles = 0
    for g in os.scandir(fpath):
        if g.is_file(): numFiles += 1

    for findex in range(numFiles):  
        with open(fpath + fname + str(findex) + '.dat') as f:
            line = f.readline()
            while 'BeginData' not in line:
                if 'ORIGIN_POSITION' in line:
                    splitLine = line.strip().split(' ')
                    originPos = (float(splitLine[1]) * 200, float(splitLine[2]) * 200, float(splitLine[3]) * 200)

                elif 'A_AXIS_MIN' in line:
                    line = line.strip().split(' ')
                    xMin = float(line[1]) * 200

                elif 'A_AXIS_MAX' in line:
                    line = line.strip().split(' ')
                    xMax = float(line[1]) * 200

                elif 'B_AXIS_MIN' in line:
                    line = line.strip().split(' ')
                    yMin = float(line[1]) * 200

                elif 'B_AXIS_MAX' in line:
                    line = line.strip().split(' ')
                    yMax = float(line[1]) * 200

                elif 'A_AXIS_DIM' in line:
                    line = line.strip().split(' ')
                    xBins = int(line[1])

                elif 'B_AXIS_DIM' in line:
                    line = line.strip().split(' ')
                    yBins = int(line[1])

                line = f.readline()

            line = f.readline()
            dataArray = np.array(line.strip().split(' '))
            line = f.readline()
            while line.strip().split(' ') != ['']:
                dataArray = np.vstack((dataArray, np.array(line.strip().split(' '))))
                line = f.readline()

            dataArray = dataArray.astype(float)
            plotDataL[originPos] = np.sum(dataArray[:, :])

    #plt.clf()
    plt.gca().set_aspect('auto')

    planeL = list(plotDataL.keys())
    irradL = {pos[2]: plotDataL[pos] for pos in planeL}
    sortedL = sorted(irradL.items())[:]    
    zL, fL = zip(*sortedL)

    nRaysL = [irrad * 10**8 * ((xMax - xMin) / (xBins * 200))**2 for irrad in fL]
    errL = np.sqrt(nRaysL) * 10**-8 / ((1 / 21) ** 2)
    errL = np.sqrt(nRaysL) * 10**-8
    nRaysL = [num * 10**-8 for num in nRaysL]

    #plt.errorbar(zL, nRaysL, errL, fmt = '+', label = labels[fpath])
    plt.scatter(zL, nRaysL, marker = '+', label = labels[fpath])
    #plt.plot(zL, nRaysL, label = labels[fpath])

plt.title('Prop. of Rays Recorded by XL-SNSPD for Various Geometries Along z-axis')
plt.xlabel('z Shift from Focus (mm)')
plt.ylabel('Power')
plt.ylabel('Prop. of Total Rays')
plt.xticks(np.arange(-20, 20.1, step=4))
plt.legend()
plt.savefig('BlackbodyPlots/poster-plot.png')
