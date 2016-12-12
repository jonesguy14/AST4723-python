import numpy as np
import sys
import matplotlib.pyplot as plt
from astropy.io import fits

# Get the input from the command line
# Files are already bias-subtracted
#files = sys.argv[1:]
#print(files)

f = fits.open("masterSpectArgon.fit")
spectData = f[0].data
f.close()

dataAtColumns = np.zeros(1000)#spectData.shape[1])
for c in range(1000):#spectData.shape[1]):
	for r in range(400,500):#spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]

scale = np.arange(0, len(dataAtColumns), 1)
#for i in range(len(scale)):
#	scale[i] = -0.2067 * scale[i] + 577.76
plt.plot(scale, dataAtColumns)

print("is nan : ",np.any(np.isnan(dataAtColumns)))
for i in range(len(dataAtColumns)):
	print("pixel:{:5d}, count:{:12.2f}".format(i, dataAtColumns[i]))
	if np.isnan(dataAtColumns[i]):
		dataAtColumns[i] = (dataAtColumns[i-1])

plt.xlabel('Pixel')
plt.ylabel('Counts')
plt.title('Argon Spectroscopy')
plt.grid(True)
plt.savefig("ArgonPlot.png")
plt.close()

f = fits.open("masterSpectNeon.fit")
spectData = f[0].data
f.close()

dataAtColumns = np.zeros(1000)#spectData.shape[1])
for c in range(1000):#spectData.shape[1]):
	for r in range(400,500):#spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]

scale = np.arange(0, len(dataAtColumns), 1)
#for i in range(len(scale)):
#	scale[i] = -0.2067 * scale[i] + 577.76
plt.plot(scale, dataAtColumns)

print("is nan : ",np.any(np.isnan(dataAtColumns)))
for i in range(len(dataAtColumns)):
	print("pixel:{:5d}, count:{:12.2f}".format(i, dataAtColumns[i]))
	if np.isnan(dataAtColumns[i]):
		dataAtColumns[i] = (dataAtColumns[i-1])

plt.xlabel('Pixel')
plt.ylabel('Counts')
plt.title('Neon Spectroscopy')
plt.grid(True)
plt.savefig("NeonPlot.png")
plt.close()



