from __future__ import division

def image_step_clean(stepsize, img):
	'''
	Checks image rows and cols cleanly divide by a provided stepsize - if not then resample image 
	so to avoid boundary errors
	'''
	rows, cols = img.shape

	if cols%stepsize != 0 and rows%stepsize != 0 :
		#print("image in x and y must be cleanly divisible by step size... resampling rows and cols")
		new_cols = stepsize * (cols//stepsize)
		new_rows = stepsize * (rows//stepsize)
		new_img = img[0:new_rows, 0:new_cols]
		print(new_img.shape)
		return new_img

	elif cols%stepsize != 0:
		#print("image in x and y must be cleanly divisible by step size... resampling cols")
		new_cols = stepsize * (cols//stepsize)
		img = img[0:rows, 0:new_cols]
		return img

	elif rows%stepsize != 0:
		#print("image in x and y must be cleanly divisible by step size... resampling rows")
		new_rows = stepsize * (rows//stepsize)
		img = img[0:new_rows, 0:cols]
		return img

	else:
		# Image cleanly divided by step
		return img
	
if __name__ == "__main__":
	print("Run from import.")