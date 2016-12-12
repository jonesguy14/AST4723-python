import numpy as np
import sep
import sys
from math import log
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Ellipse

def convertApparentToAbsoluteM15(mag):
	return mag - 5 * (log(10301.807,10) - 1)

def convertFluxtoMag_V(flux):
	if flux < 0: 
		flux = 1
	mag = -2.5 * log(flux, 10) + 37.5279
	return convertApparentToAbsoluteM15(mag);

def convertFluxtoMag_I(flux):
	if flux < 0:
		flux = 1
	mag = -2.5 * log(flux, 10) + 37.8798
	return convertApparentToAbsoluteM15(mag);

# Put V filter image first!
files = sys.argv[1:]
print(files)

fileDataList = list()
for file in files:
	f = fits.open(file)
	fileDataList.append(f[0].data)
	f.close()

objectsList = list()
fluxList = list()
for i in range(len(fileDataList)):
	d = fileDataList[i]
	data = d.byteswap().newbyteorder()
	bkg = sep.Background(data)
	data_sub = data - bkg
	objects = sep.extract(data_sub, 3, err=bkg.globalrms, deblend_cont=0.0015) #old 1.5
	objectsList.append(objects)
	flux, fluxerr, flag = sep.sum_circle(data_sub, objects['x'], objects['y'], 3, err=bkg.globalrms, gain=1.0)
	fluxList.append(flux)
	
	# plot background-subtracted image
	fig, ax = plt.subplots()
	m, s = np.mean(data_sub), np.std(data_sub)
	im = ax.imshow(data_sub, interpolation='nearest', cmap='gray',
	               vmin=m-s, vmax=m+s, origin='lower')

	# plot an ellipse for each object
	for i in range(len(objects)):
		#if objects['npix'][i] < 1000:
	    e = Ellipse(xy=(objects['x'][i], objects['y'][i]),
	                width=6*objects['a'][i],
	                height=6*objects['b'][i],
	                angle=objects['theta'][i] * 180. / np.pi)
	    e.set_facecolor('none')
	    e.set_edgecolor('red')
	    ax.add_artist(e)
	    #print("object ",objects['x'][i])
	    print("object ({:8.2f},{:8.2f}): flux = {:9.2f} +/- {:7.2f}".format(objects['x'][i], objects['y'][i], flux[i], fluxerr[i]))

	plt.savefig("image"+str(i)+".png")

v_factor = 2497.556
i_factor = 4073.803

# Match up objects from each image
array_V = list()
array_VsubI = list()
for indexV in range(len(objectsList[0])):
	if objectsList[0][indexV]['npix'] < 1000 and objectsList[0][indexV]['x'] < 1000:
		for indexI in range(len(objectsList[1])):
			if objectsList[1][indexI]['npix'] < 1000:
				# See if obj1 x,y and obj2 x,y are close enough
				# If they are, add the pair to a final list
				if abs(objectsList[0][indexV]['x'] - objectsList[1][indexI]['x']) < 1 and abs(objectsList[0][indexV]['y'] - objectsList[1][indexI]['y']) < 1:
					#print("object ({:8.2f},{:8.2f}): flux = {:9.2f} +/- {:7.2f}".format(objects['x'][i], objects['y'][i], flux[i], fluxerr[i]))
					if convertFluxtoMag_V(fluxList[0][indexV]) - convertFluxtoMag_I(fluxList[1][indexI]) > -5:
						array_V.append(convertFluxtoMag_V(fluxList[0][indexV]))
						array_VsubI.append(convertFluxtoMag_V(fluxList[0][indexV]) - convertFluxtoMag_I(fluxList[1][indexI]))

fig, ax = plt.subplots()
ax.scatter(array_VsubI, array_V)
plt.gca().invert_yaxis()
plt.xlabel('V - I Color')
plt.ylabel('V Magnitude')
plt.title('HR Diagram, M15 Globular Cluster')
plt.grid(True)
plt.savefig("HR.png")










