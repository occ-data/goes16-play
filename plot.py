#!/usr/bin/env python
from netCDF4 import Dataset
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

# Run this as
# ./plot.py <MCMIP netcdf file> <output.png>

if len(sys.argv) < 2:
	print "Usage: ./plot.py <MCMIP netcdf file> <output.png>"
	sys.exit()

# Open the NetCDF File
g16nc = Dataset(sys.argv[1], 'r')
band1 = g16nc.variables['CMI_C01'][:]

# Get the Blue, Red, and Veggie bands + gamma correct
ref_blue = np.ma.array(np.sqrt(g16nc.variables['CMI_C01'][:]), mask=test.mask)
ref_red = np.ma.array(np.sqrt(g16nc.variables['CMI_C02'][:]), mask=test.mask)
ref_veggie = np.ma.array(np.sqrt(g16nc.variables['CMI_C03'][:]), mask=test.mask)

# Make the green band using a linear relationship
ref_green = np.ma.copy(ref_veggie)
gooddata = np.where(ref_veggie.mask == False)
ref_green[gooddata] = 0.48358168 * ref_red[gooddata] + 0.45706946 * ref_blue[gooddata] + 0.06038137 * ref_veggie[gooddata]

# Prepare the Clean IR band by converting brightness temperatures to greyscale values
cleanir = g16nc.variables['CMI_C13'][:]
cir_min = 90.0
cir_max = 313.0
cleanir_c = (cleanir - cir_min) / (cir_max - cir_min)
cleanir_c = np.maximum(cleanir_c, 0.0)
cleanir_c = np.minimum(cleanir_c, 1.0)
cleanir_c = 1.0 - np.float64(cleanir_c)

# Make an alpha mask so off Earth alpha = 0
mask = np.where(band1.mask == True)
alpha = np.ones(band1.shape)
alpha[mask] = 0.0
blended = np.dstack([np.maximum(ref_red, cleanir_c), np.maximum(ref_green, cleanir_c), np.maximum(ref_blue, cleanir_c), alpha])

# Plot it! Without axis & labels
fig = plt.figure(figsize=(6,6),dpi=300)
plt.imshow(blended)
plt.axis('off')
fig.gca().set_axis_off()
fig.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
fig.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())
fig.savefig(sys.argv[2], transparent=True, bbox_inches = 'tight', pad_inches = 0)
plt.clf()
