import cv2
import numpy as np
from matWrp import MatWrp
from core import Core

def _resize_width(inWrp, delta):
    if delta == 0:
        return
    energy_wrp = MatWrp()
    energy_wrp.blank_image(inWrp.row(), inWrp.col(), inWrp.mat.dtype)
    energy_wrp.set_orientation(inWrp)

    energy_wrp.mat = filter(inWrp.mat)

    core = Core()
    seams = core.get_seams(energy_wrp, abs(delta))
    core.process_seams(inWrp, seams, delta < 0)

def filter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3,3),np.float64)/9
    dst = cv2.filter2D(gray,-1,kernel)

    gray_sobelx = cv2.Sobel(dst,cv2.CV_32F,1,0)
    gray_sobely = cv2.Sobel(dst,cv2.CV_32F,0,1)

    gray_abs_sobelx = cv2.convertScaleAbs(gray_sobelx) 
    gray_abs_sobely = cv2.convertScaleAbs(gray_sobely)

    gray_sobel_edge = cv2.addWeighted(gray_abs_sobelx,0.5,gray_abs_sobely,0.5,0) 

    return gray_sobel_edge

def resize(image, height, width):
    orig_w = image.shape[0] #col
    orig_h = image.shape[1] #row

    h_delta = height - orig_h
    w_delta = width - orig_w
    if h_delta < 0:
        h_delta = min(abs(h_delta), orig_h) * -1
    else:
        h_delta = min(abs(h_delta), orig_h)

    if w_delta < 0:
        w_delta = min(abs(w_delta), orig_w) * -1
    else:
        w_delta = min(abs(w_delta), orig_w)
    in_wrp = MatWrp()
    in_wrp.copy_image(image.copy())

    if (w_delta + in_wrp.width() > h_delta + in_wrp.height()):
        w_delta, h_delta = h_delta, w_delta
        print(in_wrp.mat.shape)
        in_wrp.copy_image(in_wrp.mat.transpose(1,0,2))
        print(in_wrp.mat.shape)
        in_wrp.transpose = not in_wrp.transpose

    _resize_width(in_wrp, w_delta)
    in_wrp.copy_image(in_wrp.mat.transpose(1,0,2))
    in_wrp.transpose = not in_wrp.transpose
    _resize_width(in_wrp, h_delta)
    return in_wrp.mat


if __name__ == '__main__':
    im = cv2.imread('a.png')
    out = resize(im, 688, 200)