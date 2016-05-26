from __future__ import division
import os
import sys

from osgeo import gdal, gdalconst 
from osgeo.gdalconst import * 

import util
# Register driver
#gdal.AllRegister() #<-- useful only if reading in 
driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
driver.Register()

def ENVI_raster_binary_to_2d_array(file_name):
	'''
	Converts a binary file of ENVI type to a numpy arra.
	Lack of an ENVI .hdr file will cause this to crash.

	VARIABLES
	file_name : file name and path of your file

	RETURNS
	geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name
	'''
	driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
	driver.Register()

	inDs = gdal.Open(file_name, GA_ReadOnly)
	
	if inDs is None:
		print "Couldn't open this file: " + file_name
		print '\nPerhaps you need an ENVI .hdr file? A quick way to do this is to just open the binary up in ENVI and one will be created for you.'
		sys.exit("Try again!")
	else:
		print "%s opened successfully" %file_name
		
		#print '~~~~~~~~~~~~~~'
		#print 'Get image size'
		#print '~~~~~~~~~~~~~~'
		cols = inDs.RasterXSize
		rows = inDs.RasterYSize
		bands = inDs.RasterCount
	
		#print "columns: %i" %cols
		#print "rows: %i" %rows
		#print "bands: %i" %bands
	
		#print '~~~~~~~~~~~~~~'
		#print 'Get georeference information'
		#print '~~~~~~~~~~~~~~'
		geotransform = inDs.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
	
		#print "origin x: %i" %originX
		#print "origin y: %i" %originY
		#print "width: %2.2f" %pixelWidth
		#print "height: %2.2f" %pixelHeight
	
		# Set pixel offset.....
		#print '~~~~~~~~~~~~~~' 
		#print 'Convert image to 2D array'
		#print '~~~~~~~~~~~~~~'
		band = inDs.GetRasterBand(1)
		image_array = band.ReadAsArray(0, 0, cols, rows)
		image_array_name = file_name
		#print type(image_array)
		#print image_array.shape
		
		return geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name

def load_envi(file_name):
	'''
	Loads an ENVI binary as a numpy image array also returning a tuple including map and projection info

	VARIABLES
	file_name : file name and path of your file

	RETURNS
	image_array, post, (geotransform, inDs)
	'''
	geotransform, inDs, _, _, _, _, _, post, _, image_array, _ = ENVI_raster_binary_to_2d_array(file_name)
	return image_array, post, (geotransform, inDs)

# Prerequisite to "ENVI_raster_binary_from_2d_array" if output image is different to original input for which geotransform was set
def xy_dimensions_Geotransform_update(geotransform, image_in_x_px, image_in_y_px, new_x_px, new_y_px):
	'''
	DEPRECATED: JUST USE ENVI_raster_binary_from_2d_array
	
	Recalculates xy dimensions of an image following resampling 
	- prior step to outputting a resampled array as a binary
	'''		
	print "Updating pixelHeight and Width values"
	pixelWidth_original = geotransform[1]
	pixelHeight_original = geotransform[5]
	pixel_width_new_image = (image_in_x_px * pixelWidth_original) / new_x_px ## gives pixel size in metres
	pixel_height_new_image =  (image_in_y_px * pixelHeight_original) / new_y_px ## gives pixel size in metres
	
	return pixel_width_new_image, pixel_width_new_image


## Creates an output image as an ENVI binary - this can be a different size to the original input image from which the output array has been developed
## When vieiwing in ENVI, if the image is smaller, you'll need to increase the magnification to view it - a geographic link will be possible (but not just a spatial link)

def ENVI_raster_binary_from_2d_array(envidata, file_out, post, image_array):
	'''
	Converts a numpy array back to an ENVI binary - requires geotransform and projection 
	information as imported using ENVI_raster_binary_to_2d_array() or load_ENVI(). If 
	resampling has taken place between the initial ENVI load (for which getransform and 
	projection info is specific) then the new posting size must also be passed in to 
	enable rescaling of pixels accordingly 
	'''
	util.check_output_dir(file_out)
	original_geotransform, inDs = envidata

	rows, cols = image_array.shape
	bands = 1

	# Creates a new raster data source
	outDs = driver.Create(file_out, cols, rows, bands, gdal.GDT_Float32)
	
	# Write metadata
	originX = original_geotransform[0]
	originY = original_geotransform[3]

	outDs.SetGeoTransform([originX, post, 0.0, originY, 0.0, -post])
	outDs.SetProjection(inDs.GetProjection())

	#Write raster datasets
	outBand = outDs.GetRasterBand(1)
	outBand.WriteArray(image_array)
	
	new_geotransform = outDs.GetGeoTransform()
	new_projection = outDs.GetProjection()
	
	print "Output binary saved: ", file_out
	
	return new_geotransform,new_projection,file_out

if __name__ == "__main__":
	print("Run from import.")

