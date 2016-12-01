import numpy as np
import sys
from astropy.io import fits

files = sys.argv[1:]
print(files)

darkName = input('Enter master dark image name (use quotes): ')
darkImage = fits.open(darkName)
darkData = darkImage[0].data

flatName = input('Enter master flat image name (use quotes): ')
flatImage = fits.open(flatName)
flatData = flatImage[0].data

for file in files:
	f = fits.open(file)
	newData = f[0].data - darkData
	newData = newData/flatData

	pathSplit = file.split("/")
	imgName = pathSplit[0] + "/darkflat" + pathSplit[1]
	print(imgName)
	
	hduImage = fits.PrimaryHDU(newData)
	hduImage.writeto(imgName)
	f.close()




