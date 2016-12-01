import numpy as np
import sys
from astropy.io import fits

# Get the file name from the command line
fileStr = sys.argv[1]

# Open the FITS file via astropy.io
fileFits = fits.open(fileStr)

# Add a comment to the header
fileFits[0].header.add_comment("File modified by jonesMiniScript.py")

# Iterate through each data point in the image, setting it to zero if its negatvie
for (x,y), count in np.ndenumerate(fileFits[0].data):
	if count < 0:
		count = 0

# Calculate the mean
fileMean = np.mean(fileFits[0].data)
print("Mean is " + str(fileMean))