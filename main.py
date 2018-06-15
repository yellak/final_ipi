import recovering_color as rec
import incorporacao as inc
import simulador_distorcao as sdist
import cv2
import sys
import glob


if __name__ == "__main__":
        printar = 0

        if '-p' in sys.argv:
                printar = 1

        if '--all' in sys.argv:
                for fl in glob.glob("Imagens/*.png"):
                        inc.incorporar_cor(fl[8:], printar)
                        rec.color_recover(fl[8:], printar)

        else:
                print("Digite o nome da imagem que você deseja transformar:")
                img_name = input()

                inc.incorporar_cor(img_name, printar)
                # img = cv2.imread('Texturizadas/%s' % img_name, 0)
                # img = sdist.simulacao(img)
                # cv2.imwrite('Texturizadas/teste.png', img)
                rec.color_recover(img_name, printar)
