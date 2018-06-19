import color_recovering as rec
import color_incorporation as inc
import distortion_simulator as sdist
import matplotlib.pyplot as plt
import cv2
import sys
import glob
import numpy as np

PLOT_GRAPHICS = 1
NOT_PLOT_PSNR = 2


# Função para mostrar o valor PSNR obitido
def print_PNR(img_origin, img_result):
    psnr = 0

    Bo, Go, Ro = cv2.split(img_origin)
    Br, Gr, Rr = cv2.split(img_result)
    conc_origin = np.concatenate((Bo, Go, Ro))
    conc_result = np.concatenate((Br, Gr, Rr))
    psnr += cv2.PSNR(conc_origin, conc_result)

    print("O valor Peak-SNR obtido foi:")
    print("%.3f" % psnr)


# Função para plotar os resultados obtidos
def print_(img_origin, img_text, img_result):

    plt.subplot(131)
    plt.imshow(cv2.cvtColor(img_origin, cv2.COLOR_BGR2RGB))
    plt.title("Imagem original")
    plt.axis('off')
    plt.subplot(132)
    plt.imshow(img_text, cmap='gray')
    plt.title("Imagem Texturizada")
    plt.axis('off')
    plt.subplot(133)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title("Imagem Resultante")
    plt.axis('off')
    plt.show()


# Parte principal do programa
if __name__ == "__main__":
    printar = 0

    # Flag para printar os resultados
    if '-p' in sys.argv:
        printar = 1

    # Flag para realizar o processo para todas as imagens
    if '--all' in sys.argv:
        print("Processando para todas as imagens da pasta ", end = "")
        print("Imagens...")
        printar = NOT_PLOT_PSNR
        for fl in glob.glob("Imagens/*.png"):
            print("Imagem %s..." % fl[8:], end = " ")
            img = cv2.imread('Imagens/%s' % fl[8:])
            img_text = inc.color_incorporation(img)

            # Salvando a imagem resultante
            cv2.imwrite("Texturizadas/%s" % fl[8:], img_text)

            img_rec = rec.color_recover(img_text, img.shape)

            # converte a imagem recuperada para BGR
            img_rec = inc.Convert_YCC2BGR(img_rec)
            cv2.imwrite('Resultados/%s' % fl[8:], img_rec)

            img_rec = cv2.imread('Resultados/%s' % fl[8:])
            if printar == 1:
                print_(img, img_text, img_rec)
                print_PNR(img, img_rec)
            print("Feito")

    else:
        print("Digite o nome da imagem que você deseja transformar:")
        img_name = input()
        img = cv2.imread('Imagens/%s' % img_name)
        if img is None:
            print("Imagem %s não encontrada na pasta Imagens" % img_name)
            exit(1)

        # Função que irá incorporar as cores na imagem cinza
        img_text = inc.color_incorporation(img)
        # Salvando a imagem resultante
        cv2.imwrite("Texturizadas/%s" % img_name, img_text)

        # Simulação
        simulation = -1
        while(simulation < 0 or simulation > 1):
            print("\nSimular impressão?")
            print("0. Não")
            print("1. Sim")
            simulation = int(input())

        if(simulation == 1):
            k = int(input("Qual a ordem do resize?\n"))
            print("Simulando distorção por impressão...")

            img_text = cv2.imread('Texturizadas/%s' % img_name, 0)
            if img_text is None:
                print("Imgagem %s não encontrada na pasta Texturizadas" % img_name)
                exit(1)

            # Função que simulará a impressão de um documento
            img_text = sdist.print_scan(img_text, k)
            cv2.imwrite('Texturizadas/%s' % img_name, img_text)

        img_text = cv2.imread('Texturizadas/%s' % img_name, 0)
        if img_text is None:
            print("Imagem %s não encontrada na pasta Texturizadas" % img_name)
            exit(1)

        # Recuperando as cores da imagem
        img_rec = rec.color_recover(img_text, img.shape)

        # Converte a imagem recuperada para BGR
        img_rec = inc.Convert_YCC2BGR(img_rec)

        cv2.imwrite('Resultados/%s' % img_name, img_rec)
        img_rec = cv2.imread('Resultados/%s' % img_name)

        # Printando os resultados
        if printar == 1:
            print_(img, img_text, img_rec)
        print_PNR(img, img_rec)
