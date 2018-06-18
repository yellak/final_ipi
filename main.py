import color_recovering as rec
import color_incorporation as inc
import distortion_simulator as sdist
import matplotlib.pyplot as plt
import cv2
import sys
import glob

PLOT_GRAPHICS = 1
NOT_PLOT_PSNR = 2

def print_PNR(img_origin, img_result):
    psnr = 0
    img_origin = cv2.cvtColor(img_origin, cv2.COLOR_BGR2YCrCb)
    img_result = cv2.cvtColor(img_result, cv2.COLOR_BGR2YCrCb)
    
    psnr += cv2.PSNR(img_origin[:, :, 0], img_result[:, :, 0])
   
    print("O valor Peak-SNR obtido foi:")
    print("%.3f" % psnr)


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


if __name__ == "__main__":
        printar = 0

        if '-p' in sys.argv:
                printar = 1

        if '--all' in sys.argv:
                print("Processando para todas as imagens da pasta ", end="")
                print("Imagens...")
                print("Isso pode demorar um pouco")
                printar = NOT_PLOT_PSNR
                for fl in glob.glob("Imagens/*.png"):
                    img = cv2.imread('Imagens/%s' % fl[8:])
                    img_text = inc.color_incorporation(img)
                    # Salvando a imagem resultante
                    cv2.imwrite("Texturizadas/%s" % fl[8:], img_text)

                    img_rec = rec.color_recover(img_text, img.shape)

                    cv2.imwrite('Crominâncias/Y%s' % fl[8:], img_rec[:, :, 0])
                    cv2.imwrite('Crominâncias/Cr%s' % fl[8:], img_rec[:, :, 1])
                    cv2.imwrite('Crominâncias/Cb%s' % fl[8:], img_rec[:, :, 2])
    
                    # converte a imagem recuperada para BGR
                    img_rec = inc.Convert_YCC2BGR(img_rec)
                    cv2.imwrite('Resultados/%s' % fl[8:], img_rec)
            
                    img_rec = cv2.imread('Resultados/%s' % fl[8:])
                    if printar == 1:
                        print_(img, img_text, img_rec)
                        print_PNR(img, img_rec)
       
        else:
                print("Digite o nome da imagem que você deseja transformar:")
                img_name = input()
                img = cv2.imread('Imagens/%s' % img_name)
                if img is None:
                    print("Imagem %s não encontrada na pasta Imagens" % img_name)
                    exit(1)

                img_text = inc.color_incorporation(img)
                # Salvando a imagem resultante
                cv2.imwrite("Texturizadas/%s" % img_name, img_text)
               
                # simulação
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

                    img_text = sdist.print_scan(img_text, k)
                    cv2.imwrite('Texturizadas/%s' % img_name, img_text)

                img_text = cv2.imread('Texturizadas/%s' % img_name, 0)
                if img_text is None:
                    print("Imagem %s não encontrada na pasta Texturizadas" % img_name)
                    exit(1)

                img_rec = rec.color_recover(img_text, img.shape)

                cv2.imwrite('Crominâncias/Y%s' % img_name, img_rec[:, :, 0])
                cv2.imwrite('Crominâncias/Cr%s' % img_name, img_rec[:, :, 1])
                cv2.imwrite('Crominâncias/Cb%s' % img_name, img_rec[:, :, 2])

                # converte a imagem recuperada para BGR
                img_rec = inc.Convert_YCC2BGR(img_rec)
                # img_rec = cv2.cvtColor(img_rec, cv2.COLOR_YCrCb2BGR)

                cv2.imwrite('Resultados/%s' % img_name, img_rec)
                img_rec = cv2.imread('Resultados/%s' % img_name)
                
                if printar == 1:
                    print_(img, img_text, img_rec)
                    print_PNR(img, img_rec)
                      
                # else:
                #        print("\nPor favor, verifique se digitou o nome da")
                #        print("imagem corretamente e se ela está na pasta Imagens")
