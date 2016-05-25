from __future__ import division

def border_indent(kernel_size, nxwind, nywind):
	'''
	Calculates how far into an image a pixel can be sampled to ensure a full 
	kernel can be sampled. Without "stepping in" from the perimeter of a 
	given image, part of the kernel - centred around the pixel position - would 
	fall outside of the main image/array
	'''
	window_border_indent = int((kernel_size - 1)/2 )
	window_border_indent_end_X = int(nxwind - window_border_indent)
	window_border_indent_end_Y = int(nywind - window_border_indent) 
	
	return window_border_indent, window_border_indent_end_X, window_border_indent_end_Y


def window_instance_dimensions(ii, jj, window_border_indent, nxwind, nywind, kernel_size, modification_value=1):
	'''
	Calculate the max and min array coordinate positions (rows/cols) for a kernel at a given pixel position
	where window_border_indent == 0.5 * kernel size
	'''
	imin=max(0,ii-(window_border_indent*modification_value)) # gets the maximum of either 0 or i-kernel_size/2...
	imax=min(nywind-1,ii+(window_border_indent*modification_value))+1
	jmin=max(0,jj-(window_border_indent*modification_value))
	jmax=min(nxwind-1,jj+(window_border_indent*modification_value))+1
	
	calc_moving_window_size_x = imax - imin 
	calc_moving_window_size_y = jmax- jmin

	return imin, imax, jmin, jmax, calc_moving_window_size_x, calc_moving_window_size_y

if __name__ == "__main__":
	print("Run from import.")