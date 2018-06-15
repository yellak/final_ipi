import recovering_color as rec
import incorporacao as inc
import sys
import glob


if __name__ == "__main__":
        if sys.argv[1] == '--all':
                for fl in glob.glob("Imagens/*.png"):
                        inc.incorporar_cor(fl[8:])
                        rec.color_recover(fl[8:])

        else:
                print("Digite o nome da imagem que você deseja transformar:")
                img_name = input()

                inc.incorporar_cor(img_name)
                rec.color_recover(img_name)
