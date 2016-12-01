import numpy as np
import sys
import skimage.feature
import scipy.ndimage
from astropy.io import fits

# Get the input from the command line
# Files are already bias-subtracted
files = sys.argv[1:]
print(files)

baseImage = fits.open(files[0])
baseImageData = baseImage[0].data
imgName = "align_" + files[0]
print(imgName)
hduShift = fits.PrimaryHDU(baseImageData)
hduShift.writeto(imgName)

# Align all other images
for i in range(1, len(files)):
	f = fits.open(files[i])
	shift, error, diffphase = skimage.feature.register_translation(baseImageData[200:1300,300:600], f[0].data[200:1300,300:600], upsample_factor=100)
	fShift = f
	fShift[0].data = scipy.ndimage.shift(f[0].data, shift)
	hduShift = fits.PrimaryHDU(fShift[0].data)
	imgName = "align_" + files[i]
	print(imgName)
	hduShift.writeto(imgName)
	f.close()



