import cv2
import numpy as np
import pywt
from matplotlib import pyplot as plot
import PIL
from PIL import Image

if __name__ == '__main__':

	lena = cv2.imread("lena.jpg", 0)

	#transformada wavelet
	coeffs = pywt.wavedec2(lena, 'db1', level=2)
	CA1, (CH1, CV1, CD1), (CH2, CV2, CD2) = coeffs

	#transformada inversa
	#pywt.idwt2()

	ResCD1 = cv2.resize(CD1, dsize=(2 * CD1.shape[1], 2 * CD1.shape[0]), interpolation=cv2.INTER_AREA)
	'''
	Cb = np.abs(CV2) - np.abs(ResCD1)
	Cr = np.abs(CH2) - np.abs(CD2)

	#resize Cb e Cr

	Cb = cv2.resize(Cb, dsize=(2 * Cb.shape[0], 2 * Cb.shape[1]), interpolation=cv2.INTER_AREA)
	Cr = cv2.resize(Cr, dsize=(2 * Cr.shape[0], 2 * Cr.shape[1]), interpolation=cv2.INTER_AREA)
	'''
	plot.subplot(121), plot.imshow(CD1, cmap='gray')
	plot.subplot(122), plot.imshow(ResCD1, cmap='gray')
	
	'''
	plot.subplot(333), plot.imshow(CV2, cmap='gray')
	plot.subplot(334), plot.imshow(CD2, cmap='gray')
	plot.subplot(335), plot.imshow(CH1, cmap='gray')
	plot.subplot(336), plot.imshow(CV1, cmap='gray')
	plot.subplot(337), plot.imshow(CD1, cmap='gray')
	'''
	plot.show()
