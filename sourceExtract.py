import numpy as np
import sep
import sys
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Ellipse

files = sys.argv[1:]
print(files)

fileDataList = list()
for file in files:
	f = fits.open(file)
	fileDataList.append(f[0].data)
	f.close()

for d in fileDataList:
	data = d.byteswap().newbyteorder()
	bkg = sep.Background(data)
	data_sub = data - bkg
	objects = sep.extract(data_sub, 1.5, err=bkg.globalrms)
	flux, fluxerr, flag = sep.sum_circle(data_sub, objects['x'], objects['y'], 3.0, err=bkg.globalrms, gain=1.0)
	print(len(objects))
	# plot background-subtracted image
	fig, ax = plt.subplots()
	m, s = np.mean(data_sub), np.std(data_sub)
	im = ax.imshow(data_sub, interpolation='nearest', cmap='gray',
	               vmin=m-s, vmax=m+s, origin='lower')

	# plot an ellipse for each object
	for i in range(len(objects)):
	    e = Ellipse(xy=(objects['x'][i], objects['y'][i]),
	                width=6*objects['a'][i],
	                height=6*objects['b'][i],
	                angle=objects['theta'][i] * 180. / np.pi)
	    e.set_facecolor('none')
	    e.set_edgecolor('red')
	    ax.add_artist(e)
	    #print("object ",objects['x'][i])
	    print("object ({:8.2f},{:8.2f}): flux = {:9.2f} +/- {:7.2f}".format(objects['x'][i], objects['y'][i], flux[i], fluxerr[i]))

	plt.show()