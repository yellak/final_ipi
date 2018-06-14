import cv2
import numpy as np
import pywt
from matplotlib import pyplot as plot
import PIL
from PIL import Image
import incorporacao as i

if __name__ == '__main__':

	lena = cv2.imread("lena.jpg")
	ImgText = i.incorporar_cor(lena)

	#faz a transformada wavelet discreta 2d
	cv2.imshow('texturizada', ImgText)
	Coef = pywt.wavedec2(ImgText, 'db1', level=2)
	CA2, (CH2, CV2, CD2), (CH1, CV1, CD1) = Coef

	#redimensiona CD2
	
	RedCD2 = cv2.resize(CD2, dsize=(CV1.shape[1], CV1.shape[0]), interpolation=cv2.INTER_AREA)
	
	#RedCD2 = cv2.resize(CD2, dsize=(2 * CD2.shape[1], 2 * CD2.shape[0]), interpolation=cv2.INTER_AREA)

	#recupear o Cb e o Cr
	Cb = np.abs(CV1) - np.abs(RedCD2)
	Cr = np.abs(CH1) - np.abs(CD1)

	#redimensiona o Cb e o Cr
	Cb = np.uint8(cv2.resize(Cb, dsize=(2 * Cb.shape[1], 2 * Cb.shape[0]), interpolation=cv2.INTER_AREA))
	Cr = np.uint8(cv2.resize(Cr, dsize=(2 * Cr.shape[1], 2 * Cr.shape[0]), interpolation=cv2.INTER_AREA))

	#
	CH1 = np.zeros((CH1.shape[0], CH1.shape[1]))
	CV1 = np.zeros((CV1.shape[0], CV1.shape[1]))
	CD2 = np.zeros((CD2.shape[0], CD2.shape[1]))
	CD1 = np.zeros((CD1.shape[0], CD1.shape[1]))
	Coef = CA2, (CH2, CV2, CD2), (CH1, CV1, CD1)

	#recupera o Y a partir da transformada wavelet inversa
	Y = np.uint8(pywt.waverec2(Coef, 'db1'))

	#converte a imagem para BGR
	YCrCb = cv2.merge((Y, Cr, Cb))
	#ImgCorRec = np.uint8(i.Convert_YCC2BGR(YCrCb))
	ImgCorRec = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)

	cv2.imshow('Y', Y)
	#cv2.imshow('Cb', Cb)
	#cv2.imshow('Cr', Cr)
	cv2.imshow('result', ImgCorRec)
	cv2.imshow('original', lena)

#	plot.subplot(121), plot.imshow(ImgText, cmap='gray')
#	plot.subplot(122), plot.imshow(Cr, cmap='gray')

	plot.show()

	cv2.waitKey(0)
	cv2.destroyAllWindows()

