"""
@author: Dylan Pare
@name: make_mask.py
@date: 03/14/2023
@description: Create a mask to remove artifact pixels caused by e.g. edge pixels.
"""

# Import needed packages
import numpy as np
from astropy.io import fits
import os
import glob

# Get set of residstd files generated by scousepy
path = os.getcwd()
parent = os.path.dirname(path)
print(parent)
fits_dir = parent + '/HC3N_TP_7m_12m_feather/stage_4/'
rms_files = glob.glob(fits_dir + '*rms*refit.fits')
rms_names = [os.path.basename(x) for x in glob.glob(fits_dir+'*rms*refit.fits')]
aic_files = glob.glob(fits_dir + '*AIC*refit.fits')
aic_names = [os.path.basename(x) for x in glob.glob(fits_dir+'*AIC*refit.fits')]
mask_prefix = ['v0','v1','v2']

# Read in residstd file and create a mask file based on residstd threshold
for file in range(len(rms_files)):

	print(rms_names[file])
	rms_file   = rms_files[file]
	rms_image  = fits.open(rms_file)
	rms_data   = rms_image[0].data
	rms_header = rms_image[0].header

	aic_file   = aic_files[file]
	aic_image  = fits.open(aic_file)
	aic_data = aic_image[0].data
	
	mean     = np.mean(rms_data[~np.isnan(rms_data)])
	std      = np.std(rms_data[~np.isnan(rms_data)])
	print(mean)
	print(std)
	thresh_h = mean + std
	thresh_l = mean - std

	mask = np.zeros(rms_data.shape)
	for x in range(len(rms_data)):
		for y in range(len(rms_data[0])):
			if (rms_data[x][y] >= thresh_h) or (rms_data[x][y] <= thresh_l) or (aic_data[x][y] < -366.0):
				mask[x][y] = 1.0

	fits.writeto(mask_prefix[file]+'_mask.fits',data=mask,header=rms_header,overwrite=True)

