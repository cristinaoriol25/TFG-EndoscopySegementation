import cv2 
import numpy as np
from skimage.feature import hog




class frame():

    hogStimate=None
    HOGimage=None
    

    def __init__(self, path, nFrame):
        self.path=path
        self.nameFrame=nFrame        

    def imageHOG(self):
        self.hogStimate,self.HOGimage=hog(self.getFrame(), orientations=8, pixels_per_cell=(16,16), cells_per_block=(1,1), visualize=True, multichannel=True)

    def descriptorHOG(self):
        self.imageHOG()
        return self.hogStimate

    def imageColor(self):
        pixels = np.float32(self.getFrame().reshape(-1, 3))
        n_colores = 5
        criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        _, etiquetas, colores = cv2.kmeans(pixels, n_colores, None, criterio, 10, cv2.KMEANS_RANDOM_CENTERS)
        _, max = np.unique(etiquetas, return_counts=True)
        return colores[np.argmax(max)]


    def histogram(self):
        return self.histogram


    def mostrarFrame(self):
        cv2.imshow("Frame", self.getFrame())
        cv2.waitKey(0)

    def guardarFrame(self, path):
        cv2.imwrite(path+self.nameFrame, self.getFrame())

    def name(self):
        return self.nameFrame


    def __str__(self):
        cadena=self.nameFrame
        return cadena

    def getFrame(self):
        return cv2.imread(self.path+str(self.nameFrame), cv2.IMREAD_COLOR)