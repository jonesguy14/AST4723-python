# Python program to load a FITS image and display it

# import needed extensions
from numpy import *
import matplotlib.pyplot as plt # plotting package
import matplotlib.cm as cm # colormaps
from astropy.io import fits

biash = fits.open('DC_pt1s_004.FIT')
bias = biash[0].data
bias = bias.astype(int32)

h1 = fits.open('Light60s.FIT')
img1 = h1[0].data
img1 = img1.astype(int32)
img1 *= 25
img1 = subtract(img1, bias)

h2 = fits.open('Light100s.FIT')
img2 = h2[0].data
img2 = img2.astype(int32)
img2 = subtract(img2, bias)

print (img1)
print (img2)

avg = img1 + img2;
avg /= 2

avgW = avg.shape[0]
avgH = avg.shape[1]
avgSub = avg[avgW/2-50:avgW/2+50, avgH/2-50:avgH/2+50]

diff = subtract(img2, img1)
diffSub = avg[avgW/2-50:avgW/2+50, avgH/2-50:avgH/2+50]

print ('Mean: ' + str(mean(avgSub)))
print ('Std Dev: ' + str(std(diffSub)))
