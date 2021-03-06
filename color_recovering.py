import cv2
import numpy as np
import pywt


# Função que faz todo o procedimento inverso
def color_recover(img_text, size):
    # Fazendo a transformada Wavelet discreta 2D
    Coef = pywt.wavedec2(img_text, 'db1', level=2)
    CA2, (CH2, CV2, CD2), (CH1, CV1, CD1) = Coef

    # redimensiona CD2
    RedCD2 = cv2.resize(CD2, dsize=(CV1.shape[1], CV1.shape[0]), interpolation=cv2.INTER_AREA)

    # recupear o Cb e o Cr
    Cb = np.abs(CV1) - np.abs(RedCD2)
    Cr = np.abs(CH1) - np.abs(CD1)

    # redimensiona o Cb e o Cr
    Cb = cv2.resize(Cb, dsize=(size[1], size[0]), interpolation=cv2.INTER_AREA)
    Cr = cv2.resize(Cr, dsize=(size[1], size[0]), interpolation=cv2.INTER_AREA)

    CH1 = np.zeros((CH1.shape[0], CH1.shape[1]))
    CV1 = np.zeros((CV1.shape[0], CV1.shape[1]))
    CD2 = np.zeros((CD2.shape[0], CD2.shape[1]))
    CD1 = np.zeros((CD1.shape[0], CD1.shape[1]))
    Coef = CA2, (CH2, CV2, CD2), (CH1, CV1, CD1)

    # recupera o Y a partir da transformada wavelet inversa
    Y = pywt.waverec2(Coef, 'db1')

    # garante que o Y possua o mesmo tamanho da imagem texturizada
    Y = cv2.resize(Y, dsize=(size[1], size[0]), interpolation=cv2.INTER_AREA)

    # faz o merge dos três canais
    YCrCb = np.zeros((size[0], size[1], 3), np.float32)
    YCrCb[:, :, 0] = Y
    YCrCb[:, :, 1] = Cr
    YCrCb[:, :, 2] = Cb

    # Converte a imagem recuperada para BGR
    img_rec = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)

    return img_rec
