import numpy as np
import cv2
import pywt
import matplotlib.pyplot as plt


#Converte uma imagem no modelo de cores BGR para YCrCb

def Convert_BGR2YCC(Img):

    Y = Img[:, :, 0] * 0.114 + Img[:, :, 1] * 0.587 + Img[:, :, 2] * 0.299
    Cr = 0.713 * Img[:, :, 2] - 0.713 * Y[:, :] + 128
    Cb = 0.564 * Img[:, :, 0] - 0.564 * Y[:, :] + 128

    return cv2.merge([Y, Cr, Cb])

def Convert_YCC2BGR(img):
    R = img[:,:,0] + 1.403*img[:,:,1] - 1.403*128
    G = img[:,:,0] -0.714*img[:,:,1] +0.714*128 -0.344*img[:,:,2] +0.344*128
    B = img[:,:,0] + 1.773*img[:,:,2] -1.773*128
    
    return cv2.merge([B, G, R])


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
   # ycc = Convert_BGR2YCC(img)

    # Fazendo a transformada de Wavelet da imagem em escalas de cinza
    [cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(ycc[:, :, 0], 'db1', level=2)

    # Retirando camadas
    CR0 = ycc[:, :, 1]
    CB0 = ycc[:, :, 2]

    # Ajustando as imagens
    Cr = cv2.resize(CR0, (cD1.shape[1], cD1.shape[0]), interpolation=cv2.INTER_AREA)
    Cb = cv2.resize(CB0, (cV1.shape[1], cV1.shape[0]), interpolation=cv2.INTER_AREA)

    #Cr = cv2.resize(CR0, (int(CR0.shape[1] / 2), int(CR0.shape[0] / 2)), interpolation=cv2.INTER_AREA)
    #Cb = cv2.resize(CB0, (int(CB0.shape[1] / 2), int(CB0.shape[0] / 2)), interpolation=cv2.INTER_AREA)

    # Adquirindo Cb/Cr-mais e Cb/Cr-menos
    CbPlus, CbMinus = plus_minus(Cb)
    CrPlus, CrMinus = plus_minus(Cr)
    print(CbPlus)
    print(CbMinus)

    CbMinus2 = cv2.resize(CbMinus, (cD2.shape[1], cD2.shape[0]), interpolation=cv2.INTER_AREA)

    #CbMinus2 = cv2.resize(CbMinus, (int(CbMinus.shape[1] / 2), int(CbMinus.shape[0] / 2)), interpolation=cv2.INTER_AREA)

    # Substituindo as imagens obtidas na Wavelet
    cH1 = CrPlus
    cV1 = CbPlus
    cD1 = CrMinus
    cD2 = CbMinus2
    

    Coef = cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)
    img_back = pywt.waverec2(Coef, 'db1')

    return img_back
