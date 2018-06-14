import cv2
import numpy as np
import pywt
from matplotlib import pyplot as plot
import PIL
from PIL import Image

if __name__ == '__main__':

	ImgText = cv2.imread("lena.jpg", 0)

	#transformada wavelet discreta 2d
	Coef = pywt.wavedec2(ImgText, 'db1', level=2)
	CA1, (CH1, CV1, CD1), (CH2, CV2, CD2) = Coef

	#redimensiona CD1
	RedCD1 = cv2.resize(CD1, dsize=(2 * CD1.shape[1], 2 * CD1.shape[0]), interpolation=cv2.INTER_AREA)

	#Recupear o Cb e o Cr
	Cb = np.abs(CV2) - np.abs(RedCD1)
	Cr = np.abs(CH2) - np.abs(CD2)

	#redimensiona o Cb e o Cr
	Cb = np.uint8(cv2.resize(Cb, dsize=(2 * Cb.shape[1], 2 * Cb.shape[0]), interpolation=cv2.INTER_AREA))
	Cr = np.uint8(cv2.resize(Cr, dsize=(2 * Cr.shape[1], 2 * Cr.shape[0]), interpolation=cv2.INTER_AREA))

	CH2 = np.zeros((CH2.shape[0], CH2.shape[1]))
	CV2 = np.zeros((CV2.shape[0], CV2.shape[1]))
	CD2 = np.zeros((CD2.shape[0], CD2.shape[1]))
	Coef = CA1, (CH1, CV1, CD1), (CH2, CV2, CD2)

	#transformada wavelet discreta 2d inversa
	Y = np.uint8(pywt.waverec2(Coef, 'db1'))

	YCrCb = cv2.merge((Y, Cr, Cb))
	ImgCorRec = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)

	cv2.imshow('Y', Y)
	cv2.imshow('Cb', Cb)
	cv2.imshow('Cr', Cr)
	cv2.imshow('result', ImgCorRec)
	
#	plot.subplot(121), plot.imshow(Cb, cmap='gray')
#	plot.subplot(122), plot.imshow(Cr, cmap='gray')
	
	'''
	plot.subplot(333), plot.imshow(CV2, cmap='gray')
	plot.subplot(334), plot.imshow(CD2, cmap='gray')
	plot.subplot(335), plot.imshow(CH1, cmap='gray')
	plot.subplot(336), plot.imshow(CV1, cmap='gray')
	plot.subplot(337), plot.imshow(CD1, cmap='gray')
	'''
	plot.show()

	cv2.waitKey(0)
	cv2.destroyAllWindows()

