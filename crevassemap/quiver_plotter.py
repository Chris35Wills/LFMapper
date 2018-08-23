from __future__ import division

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from osgeo import gdal, gdalconst # for reading in raster
from osgeo.gdalconst import * # for reading in raster

import crevassemap.raster_functions as raster_functions
import crevassemap.util as util


def quiver_plotter(orientation_binary, spacing_binary, opath, plot_title):
	
	driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
	driver.Register()
	
	orientation, _, _ = raster_functions.load_envi(orientation_binary)
	spacing, _, _ = raster_functions.load_envi(spacing_binary)

	try:
		quiver_plot(orientation, spacing, opath, plot_title)
	except:
		print("Quiver plotting failed")

def quiver_plot(orientation, spacing, opath, plot_title, filename, interact=False):
	try:
		orientation = util.trim_constant_rows_cols(orientation) #Trim image down so there is no blank border - useful if inputs have had to be resampled
		spacing = util.trim_constant_rows_cols(spacing) #Trim image down so there is no blank border - useful if inputs have had to be resampled
		
		#spacing[spacing == 0] = np.nan

		rows, cols = spacing.shape
		X,Y = np.mgrid[0:rows,0:cols]
		## convert to radians
		orientation_type = "along"
		angle = np.radians(orientation) ## converts from degrees clockwise from north to degrees anticlockwise from east (2 different conventions for angle measurment)

		## create U and V as cos and sin of the angle
		#orientation_type = "across"
		#angle = np.radians(orientation - 90.) ## converts from degrees clockwise from north to degrees anticlockwise from east (2 different conventions for angle measurment)
											  ## vectors that will be drawn now perpendicular to crevasses
		U,V = np.cos(angle), np.sin(angle)	  ## this calculates the 

		good = orientation != 0


		# set output
		plot_out = "%s_orientation_%s.png" %(plot_title, orientation_type)
		output = "%s/%s" %(opath, plot_out)

		## create figure
		#fig, ax = plt.subplots()
		#cax = ax.imshow(spacing, cmap =cm.RdPu, interpolation='none')
		#ax.quiver(Y[good], X[good], U[good], V[good], width=0.005, pivot='middle', angles='xy', scale_units='xy', scale=1.5, headwidth=0, headlength=0, headaxislength=0)	
		#ax.set_xticklabels(" ")
		#ax.set_yticklabels(" ")
		#ax.set_title(title)
		#cbar=fig.colorbar(cax)
		##plt.show()
		#plt.savefig(output, format='png', dpi=300, transparent=True)

		
		"""
		def remove_ticks(axis):
			plt.tick_params( /
			axis=axis, /         # changes apply to the x-axis
		    which='both', /      # both major and minor ticks are affected
		    bottom='off', /      # ticks along the bottom edge are off
		    top='off', /        # ticks along the top edge are off
		    labelbottom='off') # labels along the bottom edge are off
		"""

		plt.figure()
		plt.imshow(spacing, interpolation='none')
		plt.colorbar(label="Spacing")
		plt.quiver(Y[good], X[good], U[good], V[good], width=0.005, pivot='middle', angles='xy', scale_units='xy', scale=1.5, headwidth=0, headlength=0, headaxislength=0)
		plt.set_cmap('RdPu')
		#plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off') # http://stackoverflow.com/questions/12998430/remove-xticks-in-a-matplot-lib-plot
		plt.gca().xaxis.set_major_locator(plt.NullLocator())
		plt.gca().yaxis.set_major_locator(plt.NullLocator())
		#plt.savefig(output, format='png', dpi=300, transparent=True)
		plt.savefig(filename + '.png', format='png', dpi=300, transparent=True)
		
		if interact:
			plt.title("Quiver plot")
			plt.show()
		
		return orientation, spacing
	except:
		print("Quiver plotting failed")

if __name__ == "__main__":
	print("Run from import.")