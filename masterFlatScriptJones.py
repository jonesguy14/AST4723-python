import numpy as np
import sys
import glob
from astropy.io import fits

# Get the input from the command line
# Files are already bias-subtracted
files = sys.argv[1:]
print(files)

f = fits.open("masterDark_5s.fit")
darkData = f[0].data
f.close()


# Open all the images' data
fileList = list()
for file in files:
	f = fits.open(file)
	fileList.append(f[0].data - darkData)
	f.close()

# Get median of all the images
medianList = list()
for file in fileList:
	medianList.append(np.median(file))

# Find median of the medians
median = np.median(medianList)

# Normalize each image to have same median value
for i in range(len(medianList)):
	normFactor = median / medianList[i]
	fileList[i] = normFactor * fileList[i]

# Stack all image along 3rd axis, need 3D array for median command
imagesComb = np.dstack(fileList)

# Use median command on axis 2, so it take median of all the images
medianArray = np.median(imagesComb, axis=2)

# Get median of the final image so we know how to normalize
median = np.median(medianArray)

# Divide by the median so that the image is normalized to 1
medianArray = medianArray / median

# Make the header and write to image file
hduMasterFlat= fits.PrimaryHDU(medianArray)
imageName = input('Enter desired master image name: ')
hduMasterFlat.writeto(imageName)



