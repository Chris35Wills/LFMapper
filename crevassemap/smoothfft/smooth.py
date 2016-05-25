from __future__ import division
import numpy as np
import scipy.signal

kernel = np.array([[0,  1,  0],
                   [1, -4,  1],
                   [0,  1,  0]])

def smooth_fft(u):
  """
    A smoothed version of a 2d FFT, based on Moisan (2011)

    http://www.math-info.univ-paris5.fr/~moisan/papers/2009-11r.pdf
  """
  v = np.zeros_like(u)
  v[0,:] += u[-1,:] - u[0,:]
  v[-1,:] += u[0,:] - u[-1,:]
  v[:,0] += u[:,-1] - u[:,0]
  v[:,-1] += u[:,0] - u[:,-1]

  lap_u = scipy.signal.convolve2d(u, kernel, mode='same', boundary='wrap')
  dft = np.fft.fft2(lap_u - v)

  p = np.zeros_like(u)
  m, n = u.shape
  q = np.arange(m)
  r = np.arange(n)
  r, q = np.meshgrid(r, q)
  q[0,0] = 1
  r[0,0] = 1
  p = dft / (2 * np.cos(2 * np.pi * q / m) + 2 * np.cos(2 * np.pi * r / n) - 4)
  p[0,0] = 0
  return p


if __name__ == '__main__':
  import scipy.ndimage
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm
  puppy = scipy.ndimage.imread('puppy.jpg', flatten=True) * 1.0
  puppy_fft = np.fft.fft2(puppy)
  puppy_smooth_fft = smooth_fft(puppy)
  puppy_smooth = np.fft.ifft2(puppy_smooth_fft)
  plt.figure()
  plt.subplot(2,2,1)
  plt.imshow(puppy, cmap=cm.YlGnBu_r)
  plt.subplot(2,2,2)
  plt.imshow(np.log(np.abs(np.fft.fftshift(puppy_fft))))
  plt.subplot(2,2,3)
  plt.imshow(np.real(puppy_smooth), cmap=cm.YlGnBu_r)
  plt.subplot(2,2,4)
  plt.imshow(np.log(np.abs(np.fft.fftshift(puppy_smooth_fft))))
  plt.savefig('puppies.png')
  plt.show()