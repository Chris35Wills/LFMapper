from matplotlib import pyplot as plt 
import sys
sys.path.append('C:/Users/chrwil/Downloads/LFMapper-master/LFMapper-master')
from crevassemap import raster_functions, spacing, util

'''
Approximating image feature spacings using an FT approach as well as the variable size of the kernel about 
a specified pixel - once run, spacings as per window size can be considered and the most appropriate 
feature spacing chosen to approximate minimum window size when running the full 2D step FT method.

Unlike approx_feature_spacing.py this method does not have the issues associated with non square images and 
edge effects (as a whole image, including areas not of interest, is not directly being considered). Too 
large a window size should be avoided to keep the area being tested within the area of interest (too big a 
window could strectch out of the AOI)

CSV files containing kernel size and maximum associated point spacing are saved.

Modified: January 2018
'''

plotting=False
plotting_binary=0

path = 'C:/Users/chrwil/Desktop/Hofsjokull_data/hofsjokull-2008-cmb-v1'
opath= 'C:/Users/chrwil/Desktop/Hofsjokull_data/outputs_5m'
input_image = "%s/hofsjokull_FLAT_5m_SUBSET.tif" %(path)
aoi = 'hofs_5m_sub'

spectrum_n=3.0 # flattening power value (see ./understanding_the_program/test_effect_of_flattening_on_peak_identification.py for more help)

#for i in range(len(input_image)):

image_array, post, image_data = raster_functions.load_dem(input_image)

pixelWidth=image_data[0][1]

if plotting:
	plt.imshow(image_array, interpolation='none')
	plt.title('Original image')
	plt.show()

if plotting:
	image_array=image_array[0:150, 150:300]
	plt.imshow(image_array, interpolation='none')
	plt.title('Cropped image')
	plt.show()

cols,rows=image_array.shape

if(cols != rows):
	print("Approximating centre row and column...")	

centre_col = cols//2 # gets an integer (the //)
centre_row = rows//2 # gets an integer (the //)

image_array[centre_row, centre_col] ## This doesn't really do anything....

nyqvist_frq = (rows-1)//2

kernel = 3
kernel_size_LIST = []
feature_spacing_m_LIST = []
snr_LIST = []

while kernel < centre_row//2 and kernel < centre_col//2:

	_, max_dist_px, snr = spacing.find_spacing_at_point(image_array, 
														centre_row, 
														centre_col, 
														kernel, 
														spectrum_n=spectrum_n, 
														show_fft=plotting_binary)	## how is the noise (spectrum_n) value chosen?
	
	max_dist_m = max_dist_px*pixelWidth

	#print "==========================="
	#print "Kernel: ", kernel
	#print "Spacing (pixels): ", max_dist_px
	#print "Spacing (m): ", max_dist_m

	kernel_size_LIST.append(kernel)
	feature_spacing_m_LIST.append(max_dist_m)
	snr_LIST.append(snr)
	## write values out to array and/or text file
	kernel = 2 * int(kernel * 1.2 / 2) + 1 ## what does this bit do??


# Write file out
fout='%s/kernel_estimation_out/kernel_spacing_%s_smooth_factor_%0.1f.csv' %(opath, aoi, spectrum_n)
util.check_output_dir(fout)


f=open(fout, 'w')
f.write("Kernel size (m), Feature spacing (m), SnR\n")
for i in range(len(kernel_size_LIST)):
	f.write("%f, %f, %f\n" %(kernel_size_LIST[i], feature_spacing_m_LIST[i], snr_LIST[i]))
f.close()	
	
## Plot data

ofigOut='%s/kernel_estimation_out/kernel_size_to_spacing_%s_smooth_factor_%0.1f.png' %(opath, aoi, spectrum_n)
util.check_output_dir(fout)

fig=plt.figure()
ax1=fig.add_subplot(111)

ax1.plot(kernel_size_LIST, feature_spacing_m_LIST, 'o', markersize=7)

ax1.set_ylim(np.min(feature_spacing_m_LIST) * 0.8, np.max(feature_spacing_m_LIST) * 1.2)
ax1.set_xlabel("Kernel size (m)")
ax1.set_ylabel("Maximum point spacing (m)")
ax1.patch.set_alpha(0.2)
ax1.zorder=2

ax2 = ax1.twinx()

ax2.bar(kernel_size_LIST, snr_LIST, color='r', fill=False, width=1.0) 
ax2.set_ylim(np.min(snr_LIST) * 0.8, np.max(snr_LIST) * 1.2)
ax2.set_ylabel('Signal-to-noise', rotation=-90, labelpad=12)
ax2.zorder=1

plt.savefig(ofigOut)
plt.clf()
