# This file produces the 1D and 2D plots by reading the FRED data files
# Currently configured to assume that the SNSPD is only moved in the z-dimension, but can easily be modified to accomodate 1D motion in x and y
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os


parser = argparse.ArgumentParser(description = 'FRED Data File Analyzer')
parser.add_argument('--norm', type = bool, default = False)
args = parser.parse_args()
normalized = args.norm

numFiles = 8 # Number of files in the directory below -- manual input needed
fpath = 'BlackbodyStudiesData/2024-07-25/' # Name of directory files are in -- manual input needed
fname = 'SNSPD-'

plotDataXS = {}
plotDataS = {}
plotDataM = {}
plotDataL = {}

# Reading data from files
for findex in range(numFiles):  
    with open(fpath + fname + str(findex) + '.dat') as f:
        line = f.readline()
        while 'BeginData' not in line: # Getting information about origin and size of SNSPD before data reading begins
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

        # Reading data from various subsets of the detector (XS, S, M, L)
        line = f.readline()
        dataArray = np.array(line.strip().split(' '))
        line = f.readline()
        while line.strip().split(' ') != ['']:
            dataArray = np.vstack((dataArray, np.array(line.strip().split(' '))))
            line = f.readline()

        dataArray = dataArray.astype(float)
        plotDataXS[originPos] = np.sum(dataArray[10, 10]) # Origin cell
        plotDataS[originPos] = np.sum(dataArray[8:13, 8:13]) # 5x5 array centered on origin
        plotDataM[originPos] = np.sum(dataArray[6:15, 6:15]) # 9x9 array centered on origin
        plotDataL[originPos] = np.sum(dataArray[:, :]) # Whole SNSPD

    # Making 2D plots showing the pattern of rays on the SNSPD for each data file
    xBinWidth = (xMax - xMin) / xBins
    yBinWidth = (yMax - yMin) / yBins
    xGrid = np.arange(xMin + (xBinWidth / 2), xMax + (xBinWidth / 2), xBinWidth) 
    yGrid = np.arange(yMin + (yBinWidth / 2), yMax + (xBinWidth / 2), yBinWidth)

    plt.clf()
    plt.pcolormesh(xGrid, yGrid, dataArray * 10**8 * ((xMax - xMin) / (xBins * 200))**2, cmap = 'rainbow', shading = 'nearest')
    plt.gca().set_aspect('equal')
    plt.colorbar()
    plt.title('Number of Rays on the SNSPD at z = {0}mm'.format(round(originPos[2], 2)))
    plt.xlabel('Local x Position (mm)')
    plt.ylabel('Local y Position (mm)')
    
    try:
        plt.savefig('BlackbodyPlots/2024-07-25/2D/testing2DGrid-{0}.png'.format(findex))
    except FileNotFoundError:
        try:
            os.mkdir('BlackbodyPlots/2024-07-25')
        except FileExistsError:
           pass 
        os.mkdir('BlackbodyPlots/2024-07-25/2D/')
        plt.savefig('BlackbodyPlots/2024-07-25/2D/testing2DGrid-{0}.png'.format(findex))

plt.clf()
plt.gca().set_aspect('auto')

# Repetitive code plotting the number of rays seen on the various detector subsets (for smallest SNSPD
planeXS = list(plotDataXS.keys())
irradXS = {pos[2]: plotDataXS[pos] for pos in planeXS} # Change pos[2] to pos[0] for variation along x-axis or pos[1] for y-axis
sortedXS = sorted(irradXS.items())    
zXS, fXS = zip(*sortedXS)

nRaysXS = [irrad * 10**8 * ((xMax - xMin) / (xBins * 200))**2 for irrad in fXS] # Taking irradiance data (what FRED produces) and converting it to a number of rays
#errXS = np.sqrt(nRaysXS) * 10**-8 / (((xMax - xMin) / (xBins * 200)) ** 2)

if normalized:
    errXS = np.sqrt(np.square(np.divide(errXS, fXS[5])), np.square(np.divide(np.multiply(errXS[10], errXS), fXS[10]**2)))
    fXS = np.multiply(fXS, 1 / fXS[5])
#plt.errorbar(zXS, fXS, yerr = errXS, fmt = 'o', label = '{0}mm x {0}mm'.format(round(2 * xMax * 1/21, 2)))

planeS = list(plotDataS.keys())
irradS = {pos[2]: plotDataS[pos] for pos in planeS}
sortedS = sorted(irradS.items())[:]    
zS, fS = zip(*sortedS)

nRaysS = [irrad * 10**8 * ((xMax - xMin) / (xBins * 200))**2 for irrad in fS]
#errS = np.sqrt(nRaysS) * 10**-8 / (((xMax - xMin) / (xBins * 200)) ** 2)
errS = np.sqrt(nRaysS) * 10**-8 # Poisson uncertainty for the number of rays divided by 10^8 to get uncertainty on the below proportion
nRaysS = [num * 10**-8 for num in nRaysS] # Dividing number of rays by 10^8 to instead get proportion of emitted rays observed by SNSPD

if normalized:
    errS = np.sqrt(np.square(np.divide(errS, fS[5])), np.square(np.divide(np.multiply(errS[10], errS), fS[10]**2)))
    fS = np.multiply(fS, 1 / fS[5])
#plt.errorbar(zS, fS, yerr = errS, fmt = 'o', label = '{0}mm x {0}mm'.format(round(2 * xMax * 5/21, 2)))

planeM = list(plotDataM.keys())
irradM = {pos[2]: plotDataM[pos] for pos in planeM}
sortedM = sorted(irradM.items())[:] 
zM, fM = zip(*sortedM)

nRaysM = [irrad * 10**8 * ((xMax - xMin) / (xBins * 200))**2 for irrad in fM]
#errM = np.sqrt(nRaysM) * 10**-8 / (((xMax - xMin) / (xBins * 200)) ** 2)
errM = np.sqrt(nRaysM) * 10**-8
nRaysM = [num * 10**-8 for num in nRaysM]

if normalized:
    errM = np.sqrt(np.square(np.divide(errM, fM[5])), np.square(np.divide(np.multiply(errM[10], errM), fM[10]**2)))
    fM = np.multiply(fM, 1 / fM[5])
#plt.errorbar(zM, nRaysM, yerr = errM, fmt = 'o', label = '{0}mm x {0}mm'.format(round(2 * xMax * 9/21, 2)))

# In my most recent set of plots for the 1mm^2 SNSPD, I only looked at the whole detector and not any subset so only this data is actually plotted
planeL = list(plotDataL.keys())
irradL = {pos[2]: plotDataL[pos] for pos in planeL}
sortedL = sorted(irradL.items())[:]    
zL, fL = zip(*sortedL)

nRaysL = [irrad * 10**8 * ((xMax - xMin) / (xBins * 200))**2 for irrad in fL]
#errL = np.sqrt(nRaysL) * 10**-8 / (((xMax - xMin) / (xBins * 200)) ** 2)
errL = np.sqrt(nRaysL) * 10**-8
nRaysL = [num * 10**-8 for num in nRaysL]

if normalized:
    errL = np.sqrt(np.square(np.divide(errL, fL[5])), np.square(np.divide(np.multiply(errL[10], errL), fL[10]**2)))
    fL = np.multiply(fL, 1 / fL[5])
plt.errorbar(zL, nRaysL, yerr = errL, fmt = 'o', linestyle = '--', label = '{0}mm x {0}mm'.format(round(2 * xMax, 2)))

if normalized:
    plt.title('Normalized Power for Various Detector Sizes Along z-axis')
    plt.xlabel('z Shift from Focus (mm)')
    plt.ylabel('Normalized Power')
    plt.xticks(np.arange(-20, 21, step=4))
    plt.legend()
    plt.savefig('BlackbodyPlots/2024-07-25/z-axis-irradiance-normalized.png')

else:
    plt.title('Prop. of Total Rays on Realistic SNSPD Along z-axis')
    plt.xlabel('z Shift from Focus (mm)')
    plt.ylabel('Power')
    plt.ylabel('Prop. of Total Rays')
    plt.xticks(np.arange(-0.2, 0.16, step=0.05)) # This has to be manually adjusted
    plt.legend()
    plt.savefig('BlackbodyPlots/2024-07-25/z-axis-irradiance.png')

    # When looking at a bigger SNSPD, I sometimes wanted to plot the origin detector cell separately from the rest
    plt.clf()
    plt.errorbar(zXS, fXS, yerr = errXS, fmt = 'o', label = '0.63mm x 0.63mm')
    plt.title('Power for Various Detector Sizes Along z-axis')
    plt.xlabel('z Shift from Focus (mm)')
    plt.ylabel('Power')
    plt.xticks(np.arange(-0.2, 0.16, step=0.05))
    plt.legend()
    #plt.savefig('BlackbodyPlots/2024-07-25/z-axis-irradiance-xs.png')

# Printing out z position with minimum photon counts and the z position above the focus where the counts increase by a factor of 2.5 w.r.t. minimum
for f in fXS, fS, fM, fL:
    zMin = zXS[np.argmin(f)]
    print("zMin: {0}".format(zMin))
    fDoubled = np.where(f > 2.5 * f[np.argmin(f)])[0]
    zDoubled = np.array([zXS[int(idx)] for idx in fDoubled])
    topOfValley = zDoubled[min(np.where(zDoubled > 0)[0])]
    print("Top of Valley: {0}".format(topOfValley))
