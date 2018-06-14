import numpy as np
import cv2
import pywt
import matplotlib.pyplot as plt


# Função que calcula Cb/Cr-menos e mais
def plus_minus(img):
    height, width = img.shape

    plus = np.zeros((height, width), np.uint8)
    minus = np.zeros((height, width), np.uint8)

    for y in range(0, height):
        for x in range(0, width):
            if img[y, x] > 0:
                plus[y, x] = img[y, x]
            else:
                minus[y, x] = img[y, x]

    return plus, minus


def incorporar_cor(img):
    # Convertendo a imagem
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    # Fazendo a transformada de Wavelet da imagem em escalas de cinza
    [cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(ycc[:, :, 0], 'db1', level=2)

    # Retirando camadas
    CR0 = ycc[:, :, 1]
    CB0 = ycc[:, :, 2]

    # Ajustando as imagens
    Cr = cv2.resize(CR0, (int(CR0.shape[0]/2), int(CR0.shape[1]/2)), interpolation=cv2.INTER_AREA)
    Cb = cv2.resize(CB0, (int(CB0.shape[0]/2), int(CB0.shape[1]/2)), interpolation=cv2.INTER_AREA)

    # Adquirindo Cb/Cr-mais e Cb/Cr-menos
    CbPlus, CbMinus = plus_minus(Cb)
    CrPlus, CrMinus = plus_minus(Cr)

    CbMinus2 = resize(CbMinus, (int(CbMinus.shape[0]/2), int(CbMinus.shape[1]/2)), interpolation=cv2.INTER_AREA)

    # Substituindo as imagens obtidas na Wavelet
    cH1 = CrPlus
    cV1 = CbPlus
    cD1 = CrMinus
    cD2 = CbMinus2

    img_back = pywt.waverec2([cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)], 'db1')
