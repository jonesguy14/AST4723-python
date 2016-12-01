import numpy as np
import sys
import scipy.stats
from astropy.io import fits

# Get the input from the command line
# Files are already bias-subtracted
files = sys.argv[1:]
print(files)

fileDataList = list()
for file in files:
	f = fits.open(file)
	fileDataList.append(f[0].data)
	f.close()

arrayData = np.asanyarray(fileDataList[0])
arrayShape = arrayData.shape
print(arrayShape)
rows = arrayShape[0]
columns = arrayShape[1]
stackImageData = np.zeros(arrayShape)

# Stack images
for r in range(0, rows):
	if r % 25 == 0:
		print("row: ", r)
	for c in range(0, columns):
		dataList = list()
		for i in range(0, len(fileDataList)):
			dataList.append(fileDataList[i][r][c])
		#print(dataList)
		clippedDataList, low, up = scipy.stats.sigmaclip(dataList, 2, 2)
		#print(clippedDataList)
		if len(clippedDataList) == 0:
			avgClipped = np.median(dataList)
		else:
			avgClipped = np.mean(clippedDataList)
		stackImageData[r][c] = avgClipped

# Save image
hduResult = fits.PrimaryHDU(stackImageData)
imageName = input('Enter desired result image name (use quotes): ')
hduResult.writeto(imageName)


