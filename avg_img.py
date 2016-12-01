# Python program to load a FITS image and display it

# import needed extensions
from numpy import *
import matplotlib.pyplot as plt # plotting package
import matplotlib.cm as cm # colormaps
from astropy.io import fits


# read in the files
# change the file names as appropriate
name = 'Dark_100s'
h1 = fits.open(name+'_001.FIT')

# copy the image data into a numpy (numerical python) array
img = h1[0].data

for i in range(2, 4):
	h1 = fits.open(name+'_00'+str(i)+'.FIT')
	img += h1[0].data

# divide the data by num images
img /= 3

h1 = fits.open(name+'_002.FIT')
img1_data = h1[0].data

img = img.astype(int16)
img1_data = img1_data.astype(int16)

print(img1_data)
print(img)

img = subtract(img1_data, img)

print (img)
print ("Std dev: " + str(std(img)))

plt.ion() # do plots in interactive mode
colmap = plt.get_cmap('gray') # load gray colormap

# plot the difference image
plt.figure(1)
plt.imshow(img, cmap=colmap) # plot image using gray colorbar

#plt.show(block=True) # display the images