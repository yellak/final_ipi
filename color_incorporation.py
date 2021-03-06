import numpy as np
import cv2
import pywt


# Converte uma imagem no modelo de cores BGR para YCrCb
def Convert_BGR2YCC(img):
    Y = img[:, :, 0] * 0.114 + img[:, :, 1] * 0.587 + img[:, :, 2] * 0.299
    Cr = 0.713 * img[:, :, 2] - 0.713 * Y[:, :]
    Cb = 0.564 * img[:, :, 0] - 0.564 * Y[:, :]

    return cv2.merge([Y, Cr, Cb])


# Função que calcula Cb/Cr-menos e mais
def plus_minus(img):
    height, width = img.shape

    plus = np.zeros((height, width), np.float32)
    minus = np.zeros((height, width), np.float32)
    # separa a matriz em suas partes negativa e positiva
    minus = (img - np.abs(img)) / 2
    plus = (img + np.abs(img)) / 2

    return plus, minus


# Função que irá criar a imagem texturizada
def color_incorporation(img):

    ycc = Convert_BGR2YCC(img)
    #ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    # Fazendo a transformada de Wavelet da imagem em escalas de cinza
    [cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(ycc[:, :, 0], 'db1', level=2)

    # Retirando camadas
    CR0 = ycc[:, :, 1]
    CB0 = ycc[:, :, 2]

    # Ajustando as imagens
    Cr = cv2.resize(CR0, (cD1.shape[1], cD1.shape[0]), interpolation=cv2.INTER_AREA)
    Cb = cv2.resize(CB0, (cV1.shape[1], cV1.shape[0]), interpolation=cv2.INTER_AREA)

    # Adquirindo Cb/Cr-mais e Cb/Cr-menos
    CbPlus, CbMinus = plus_minus(Cb)
    CrPlus, CrMinus = plus_minus(Cr)

    CbMinus2 = cv2.resize(CbMinus, (cD2.shape[1], cD2.shape[0]), interpolation=cv2.INTER_AREA)

    # Substituindo as imagens obtidas na Wavelet
    cH1 = CrPlus
    cV1 = CbPlus
    cD1 = CrMinus
    cD2 = CbMinus2

    Coef = cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)
    img_back = pywt.waverec2(Coef, 'db1')

    return img_back
