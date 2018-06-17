import cv2
import numpy as np
import pywt
import matplotlib.pyplot as plt
import color_incorporation as inc

PLOT_GRAPHICS = 1
NOT_PLOT_PSNR = 2


# Função que faz todo o procedimento inverso
def color_recover(name, printar):
        ImgText = cv2.imread('Texturizadas/%s' % name, 0)
        if ImgText is None:
                print("Imagem %s não encontrada na pasta Texturizadas" % name)
                return -1

        # ImgText = np.float32(ImgText)

        # Fazendo a transformada Wavelet discreta 2D
        Coef = pywt.wavedec2(ImgText, 'db1', level=2)
        CA2, (CH2, CV2, CD2), (CH1, CV1, CD1) = Coef

        # redimensiona CD2
        RedCD2 = cv2.resize(CD2, dsize=(CV1.shape[1], CV1.shape[0]), interpolation=cv2.INTER_AREA)

        # recupear o Cb e o Cr
        Cb = np.abs(CV1) - np.abs(RedCD2)
        Cr = np.abs(CH1) - np.abs(CD1)

        # redimensiona o Cb e o Cr
        Cb = cv2.resize(Cb, dsize=(2 * Cb.shape[1], 2 * Cb.shape[0]), interpolation=cv2.INTER_AREA)
        Cr = cv2.resize(Cr, dsize=(2 * Cr.shape[1], 2 * Cr.shape[0]), interpolation=cv2.INTER_AREA)

        CH1 = np.zeros((CH1.shape[0], CH1.shape[1]))
        CV1 = np.zeros((CV1.shape[0], CV1.shape[1]))
        CD2 = np.zeros((CD2.shape[0], CD2.shape[1]))
        CD1 = np.zeros((CD1.shape[0], CD1.shape[1]))
        Coef = CA2, (CH2, CV2, CD2), (CH1, CV1, CD1)

        # recupera o Y a partir da transformada wavelet inversa
        Y = pywt.waverec2(Coef, 'db1')

        # Converte a imagem para BGR
        YCrCb = np.zeros((Y.shape[0], Y.shape[1], 3), np.float32)
        YCrCb[:, :, 0] = Y
        YCrCb[:, :, 1] = Cr
        YCrCb[:, :, 2] = Cb
        ImgCorRec = inc.Convert_YCC2BGR(YCrCb)

        cv2.imwrite('Crominâncias/Y%s' % name, Y)
        cv2.imwrite('Crominâncias/Cr%s' % name, Cr)
        cv2.imwrite('Crominâncias/Cb%s' % name, Cb)
        cv2.imwrite('Resultados/%s' % name, ImgCorRec)

        if printar == PLOT_GRAPHICS:
                ImgCorRec = cv2.imread('Resultados/%s' % name)
                ImgCorRec = cv2.cvtColor(ImgCorRec, cv2.COLOR_BGR2RGB)
                plt.imshow(ImgCorRec)
                plt.title("Imagem Resultante")
                plt.axis('off')

                plt.show()

        img_origin = cv2.imread('Imagens/%s' % name)
        img_result = cv2.imread('Resultados/%s' % name)

        if printar != NOT_PLOT_PSNR:
                psnr = 0
                for i in range(0, 3):
                        psnr += cv2.PSNR(img_origin[:, :, i], img_result[:, :, i])
                psnr /= 3

                print("O valor Peak-SNR obtido foi:")
                print("%.3f" % psnr)

        return 1
