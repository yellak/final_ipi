import color_incorporation as inc
import color_recovering as rec
import distortion_simulator as sdist
import cv2
import numpy as np
import glob


def print_PNR(img_origin, img_result):
    psnr = 0

    Bo, Go, Ro = cv2.split(img_origin)
    Br, Gr, Rr = cv2.split(img_result)
    conc_origin = np.concatenate((Bo, Go, Ro))
    conc_result = np.concatenate((Br, Gr, Rr))
    psnr += cv2.PSNR(conc_origin, conc_result)

    print("%.3f" % psnr)

    return psnr

k = 4
psnr = []
for fl in glob.glob("Imagens/*.png"):
    print(fl[8:])
    img = cv2.imread(fl)
    img_text = inc.color_incorporation(img)
    cv2.imwrite("Texturizadas/%s" % fl[8:], img_text)
    img_text = cv2.imread('Texturizadas/%s' % fl[8:], 0)
    img_text = sdist.print_scan(img_text, k)
    cv2.imwrite('Texturizadas/%s' % fl[8:], img_text)
    img_text = cv2.imread('Texturizadas/%s' % fl[8:], 0)

    img_rec = rec.color_recover(img_text, img.shape)
    img_rec = inc.Convert_YCC2BGR(img_rec)

    cv2.imwrite('Resultados/%s' % fl[8:], img_rec)
    img_rec = cv2.imread('Resultados/%s' % fl[8:])

    psnr += [print_PNR(img_rec, img)]


mean = np.mean(psnr)
print(psnr)
print(mean)
