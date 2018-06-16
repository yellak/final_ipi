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
                for fl in glob.glob("Imagens/*.png"):
                        inc.color_incorporation(fl[8:], printar)
                        sdist.print_scan(fl[8:])
                        rec.color_recover(fl[8:], printar)
                                     
        else:
                print("Digite o nome da imagem que você deseja transformar:")
                img_name = input()

                inc.color_incorporation(img_name, printar)
                sdist.print_scan(img_name)
                rec.color_recover(img_name, printar)
