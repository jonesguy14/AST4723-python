import numpy as np
import sys
import glob
from astropy.io import fits

# Get the input from the command line
files = sys.argv[1:]
print(files)

# Use glob to get all files matching the input string
# Actually don't need, seems to do it by itself if using wildcards in command line (*.gif will put all gif files in the list)
#files = glob.glob(inputStr)
#print(files)

# Open all the images' data
fileList = list()
for file in files:
	f = fits.open(file)
	fileList.append(f[0].data)
	f.close()

# Stack all image along 3rd axis, need 3D array for median command
imagesComb = np.dstack(fileList)

# Use median command on axis 2, so it take median of all the images
medianArray = np.median(imagesComb, axis=2)

# Make the header and write to image file
hduMedian = fits.PrimaryHDU(medianArray)
imageName = input('Enter desired median image name: ')
hduMedian.writeto(imageName)



