import numpy as np
import sys
import matplotlib.pyplot as plt
from astropy.io import fits

# Get the input from the command line
# Files are already bias-subtracted
files = sys.argv[1:]
print(files)

f = fits.open(files[0])
spectData = f[0].data
f.close()

dataAtColumns = np.zeros(spectData.shape[1])
for c in range(spectData.shape[1]):
	for r in range(spectData.shape[0]):
		if np.isnan(spectData[r][c]):
			dataAtColumns[c] = dataAtColumns[c] + 65535
		else:
			dataAtColumns[c] = dataAtColumns[c] + spectData[r][c]
		

#for i in range(425, 475):
#	dataAtColumns[i] = 460000

scale = np.arange(0, len(dataAtColumns), 1)
for i in range(len(scale)):
	scale[i] = -0.2048 * scale[i] + 577.329
plt.plot(scale, dataAtColumns)

print("is nan : ",np.any(np.isnan(dataAtColumns)))
for i in range(len(dataAtColumns)):
	print("pixel:{:5d}, count:{:12.2f}".format(i, dataAtColumns[i]))
	if np.isnan(dataAtColumns[i]):
		dataAtColumns[i] = (dataAtColumns[i-1])

plt.xlabel('wavelength')
plt.ylabel('counts')
plt.title('Simple Spectroscopy')
plt.grid(True)
plt.savefig("test.png")
plt.show()



