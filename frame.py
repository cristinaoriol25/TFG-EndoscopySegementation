import cv2 
from utils import calculateHOG



class frame():

    hogStimate=None
    HOGimage=None

    def __init__(self, path, nFrame):
        self.path=path
        self.nameFrame=nFrame
        self.frame=cv2.imread(path+str(self.nameFrame), cv2.IMREAD_COLOR)
        

    def imageHOG(self):
        self.HOGimage=calculateHOG(self.frame)
        return self.hogStimate

    def descripHOG(self):
        hog=cv2.HOGDescriptor()
        h=hog.compute(self.frame)
        return h.ravel()


    def mostrarFrame(self):
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(0)


    def name(self):
        return self.nameFrame


    def __str__(self):
        cadena=self.nameFrame
        return cadena