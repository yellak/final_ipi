import cv2
import numpy as np


# Função que aplica uma difusão de erros usando o método de Floyd-Steinberg.
def error_diffusion(img, size=(1, 1)):
        img = np.float32(img)
        #coloca uma borda preta na imagem
        img_exp = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
        img_exp[1:img.shape[0] + 1, 1:img.shape[1] + 1] = img[:, :]

        for y in range(1, size[1] + 1):
                for x in range(1, size[0] + 1):
                        old_pixel = img_exp[x, y]
                        if old_pixel > 127:
                            img_exp[x, y] = 255
                        else:
                            img_exp[x, y] = 0
                        quant_error = old_pixel - img_exp[x, y]
                        img_exp[x + 1, y] = img_exp[x + 1, y] + 7 / 16.0 * quant_error
                        img_exp[x - 1, y + 1] = img_exp[x - 1, y + 1] + 3 / 16.0 * quant_error
                        img_exp[x, y + 1] = img_exp[x, y + 1] + 5 / 16.0 * quant_error
                        img_exp[x + 1, y + 1] = img_exp[x + 1, y + 1] + 1 / 16.0 * quant_error

        #retira borda
        img[:, :] = img_exp[1:img.shape[0] + 1, 1:img.shape[1] + 1]

        return np.uint8(img)


# Função que simula a distorção gerada pelo processo
# de impressão seguida de digitalização
def print_scan(img, K=1):

        # redimensiona a imagem
        resized_img = cv2.resize(img, (K * img.shape[1], K * img.shape[0]), interpolation=cv2.INTER_AREA)

        # aplica um error diffusion
        resized_img = error_diffusion(resized_img, resized_img.shape)
        # aplica um filtro de média
        kernel = np.ones((5, 5), np.float32) / (5**2)
        resized_img = cv2.filter2D(resized_img, -1, kernel)
        resized_img = np.uint8(resized_img)
        # volta a imagem para o tamanho original
        img = cv2.resize(resized_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)


        return img
