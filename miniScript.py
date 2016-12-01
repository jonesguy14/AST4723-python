import numpy as np
import sys
from astropy.io import fits

fileStr = sys.argv[1]

print(fileStr)

fileFits = fits.open(fileStr)

fileFits[0].header.add_comment("Modified by miniScript.py")

for (x,y), count in np.ndenumerate(fileFits[0].data):
	if count < 0:
		count = 0

fileMean = np.mean(fileFits[0].data)
print("Mean is " + str(fileMean))



