import numpy as np
import sys
from astropy.io import fits

files = sys.argv[1:]
print(files)

image1 = fits.open(files[0])
image2 = fits.open(files[1])

subtractData = image1[0].data - image2[0].data

hduResult = fits.PrimaryHDU(subtractData)
imageName = input('Enter desired result image name: ')
hduResult.writeto(imageName)


