import cv2
import numpy as np


#Difusão de erros usando o método de Floyd-Steinberg.
def error_diffusion(img, size=(1, 1)):
	img = np.float32(img)

	for y in range(0, size[1] - 1):
		for x in range(1, size[0] - 1):
			old_pixel = img[x, y]
			img[x, y] = 255 if old_pixel > 127 else 0
			quant_error = old_pixel - img[x, y]
			img[x + 1, y] = img[x + 1, y] + 7 / 16.0 * quant_error
			img[x - 1, y + 1] = img[x - 1, y + 1] + 3 / 16.0 * quant_error
			img[x, y + 1] = img[x, y + 1] + 5 / 16.0 * quant_error
			img[x + 1, y + 1] = img[x + 1, y + 1] + 1 / 16.0 * quant_error
	return img


def simulacao(img, K=1):

	#redimensiona a imagem
	img = cv2.resize(img, (K * img.shape[1], K * img.shape[0]), interpolation=cv2.INTER_AREA)
	
	# aplica um error diffusion
	img = error_diffusion(img, img.shape)
	# aplica um filtro de média
	kernel = np.ones((5, 5), np.float32) / 25
	img = cv2.filter2D(img, -1, kernel)
	img = np.uint8(img)
	#volta a imagem para o tamanho original
	img = cv2.resize(img, (int(img.shape[1] / K), int(img.shape[0] / K)), interpolation=cv2.INTER_AREA)

	return img

if __name__ == '__main__':
	
	img = cv2.imread('Imagens/alegria.png', 0)
	'''
	cv2.imshow('Imagem Original', img)
	img = error_diffusion(img, img.shape)
	cv2.imshow('Imagem Halftoning', img)
	#img = Median_filter3x3(img)
	kernel = np.ones((5, 5), np.float32) / 25
	img = np.uint8(cv2.filter2D(img, -1, kernel))
	cv2.imshow('Imagem filtrada', img)
	'''
	img = simulacao(img)
	cv2.imshow('teste', img)

	cv2.waitKey(0)
	cv2.destroyAllWindows()
