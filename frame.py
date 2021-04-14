import cv2 
import numpy as np
from skimage.feature import hog




class frame():

    hogStimate=None
    HOGimage=None
    

    def __init__(self, path, nFrame):
        self.path=path
        self.nameFrame=nFrame
        self.frame=cv2.imread(path+str(self.nameFrame), cv2.IMREAD_COLOR)
        

    def imageHOG(self):
        self.hogStimate,self.HOGimage=hog(self.frame, orientations=8, pixels_per_cell=(16,16), cells_per_block=(1,1), visualize=True, multichannel=True)

    def descriptorHOG(self):
        self.imageHOG()
        return self.hogStimate

    def imageColor(self):
        pixels = np.float32(self.frame.reshape(-1, 3))
        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        return palette[np.argmax(counts)]


    def histogram(self):
        return self.histogram


    def mostrarFrame(self):
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(0)

    def guardarFrame(self, path):
        cv2.imwrite(path+self.nameFrame, self.frame)

    def name(self):
        return self.nameFrame


    def __str__(self):
        cadena=self.nameFrame
        return cadena