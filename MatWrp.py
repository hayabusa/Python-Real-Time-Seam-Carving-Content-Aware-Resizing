import cv2
import numpy as np

class MatWrp(object):
    def __init__(self):
        self.transpose = False

    def blank_image(self, width, height, type = np.float64):
        """Create new image(numpy array) filled with certain color in RGB"""
        # Create black blank image
        self.mat = np.zeros((height, width), np.float64)
        self.transpose = False

    def copy_image(self, image):
        self.mat = image
        self.transpose = False
    
    def copy_wrp(self, wrp):
        self.mat = wrp.mat
        self.mat = wrp.transpose

    def clone(self):
        newWrp = MatWrp()
        newWrp.copy_wrp(self.mat.copy())
        newWrp.transpose = self.transpose

        return newWrp

    def width(self):
        if self.transpose == False:
            return self.mat.shape[1]
        else:
            return self.mat.shape[0]
    
    def col(self):
        return self.mat.shape[0]

    def height(self):
        if self.transpose == False:
            return self.mat.shape[0]
        else:
            return self.mat.shape[1]
    
    def row(self):
        return self.mat.shape[1]


    def transpose(self):
        self.transpose = not self.transpose

    def set_shape(self, wrp):
        self.mat = np.zeros((wrp.height(), wrp.width()), np.float64)
        self.transpose = wrp.transpose

    def set_orientation(self, wrp):
        self.transpose = wrp.transpose
    
