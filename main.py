import color_recovering as rec
import color_incorporation as inc
import distortion_simulator as sdist
import cv2
import sys
import glob


if __name__ == "__main__":
        printar = 0

        if '-p' in sys.argv:
                printar = 1

        if '--all' in sys.argv:
                print("Processando para todas as imagens da pasta ", end = "")
                print("Imagens...")
                print("Isso pode demorar um pouco")
                printar = rec.NOT_PLOT_PSNR
                for fl in glob.glob("Imagens/*.png"):
                        inc.color_incorporation(fl[8:], printar)
                        rec.color_recover(fl[8:], printar)

        else:
                print("Digite o nome da imagem que você deseja transformar:")
                img_name = input()

                simulation = -1
                while(simulation < 0 or simulation > 1):
                        print("\nSimular impressão?")
                        print("0. Não")
                        print("1. Sim")
                        simulation = int(input())

                test = inc.color_incorporation(img_name, printar)

                if test != -1:
                        if(simulation == 1):
                                k = int(input("Qual a ordem do resize?\n"))
                                print("Simulando distorção por impressão...")
                                sdist.print_scan(img_name, k)

                        rec.color_recover(img_name, printar)
                else:
                        print("\nPor favor, verifique se digitou o nome da")
                        print("imagem corretamente e se ela está na pasta Imagens")
