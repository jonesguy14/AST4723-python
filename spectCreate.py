import numpy as np
import sys
import matplotlib.pyplot as plt
from astropy.io import fits

# Get the input from the command line
# Files are already bias-subtracted
#files = sys.argv[1:]
#print(files)

f = fits.open("masterSpectHR8781.fit")
spectData = f[0].data
f.close()

dataAtColumns = np.zeros(1000)#spectData.shape[1])
for c in range(1000):#spectData.shape[1]):
	for r in range(400,500):#spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]
		
# Correct for star's features
for i in range(425, 475):
	dataAtColumns[i] = 500000
for i in range(675, 700):
	dataAtColumns[i] = 340000
for i in range(790, 825):
	dataAtColumns[i] = 220000
for i in range(875, 900):
	dataAtColumns[i] = 115000

scale = np.arange(0, len(dataAtColumns), 1)
for i in range(len(scale)):
	scale[i] = -0.2017 * scale[i] + 574.13

plt.plot(scale, dataAtColumns)

print("is nan : ",np.any(np.isnan(dataAtColumns)))
for i in range(len(dataAtColumns)):
	print("pixel:{:5d}, count:{:12.2f}".format(i, dataAtColumns[i]))
	if np.isnan(dataAtColumns[i]):
		dataAtColumns[i] = (dataAtColumns[i-1])

poly = np.polyfit(scale, dataAtColumns, 9)
ffit = np.polyval(poly, scale)

plt.plot(scale, ffit)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Counts')
plt.title('HR8781 Spectroscopy')
plt.grid(True)
plt.savefig("spectHR8781.png")
plt.close()
#plt.show()

# Divide telluric data by the polyfit line
divArray = np.divide(dataAtColumns, ffit)
plt.plot(scale[0:900], divArray[0:900])
plt.xlabel('Wavelength (nm)')
plt.ylabel('Data / Polyfit')
plt.title('Data divided by Polyfit')
plt.grid(True)
plt.savefig("dataDivPolyfit.png")
plt.close()

# Open Vega file
f = fits.open("masterSpectVega.fit")
spectData = f[0].data
f.close()

# Get counts for each column of Vega
dataAtColumns = np.zeros(1000)#spectData.shape[1])
for c in range(1000):#spectData.shape[1]):
	for r in range(400,500):#spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]
	print("Vega col {:6d} = {:10.2f}".format(c, dataAtColumns[c]))

# Divide Vega data by the divArray
vegaDivArray = np.divide(dataAtColumns, divArray)

plt.plot(scale, vegaDivArray)
#plt.plot(scale, dataAtColumns)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Counts')
plt.title('Vega Spectroscopy')
plt.grid(True)
plt.savefig("spectVega.png")
plt.close()

# Open BetPeg file
f = fits.open("masterSpectBetPeg.fit")
spectData = f[0].data
f.close()

# Get counts for each column of BetPeg
dataAtColumns = np.zeros(1000)#spectData.shape[1])
for c in range(1000):#spectData.shape[1]):
	for r in range(400,500):#spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]

# Divide BetPeg data by the divArray
betpegDivArray = np.divide(dataAtColumns, divArray)

plt.plot(scale, betpegDivArray)
#plt.plot(scale, dataAtColumns)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Counts')
plt.title('BetPeg Spectroscopy')
plt.grid(True)
plt.savefig("spectBetPeg.png")
plt.close()

# Open GamCyg file
f = fits.open("masterSpectGamCyg.fit")
spectData = f[0].data
f.close()

# Get counts for each column of GamCyg
dataAtColumns = np.zeros(1000)#spectData.shape[1])
for c in range(1000):#spectData.shape[1]):
	for r in range(400,500):#spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]

# Divide GamCyg data by the divArray
gamcygDivArray = np.divide(dataAtColumns, divArray)

plt.plot(scale, gamcygDivArray)
#plt.plot(scale, dataAtColumns)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Counts')
plt.title('GamCyg Spectroscopy')
plt.grid(True)
plt.savefig("spectGamCyg.png")
plt.close()









