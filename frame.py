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
        self.hogStimate,self.HOGimage=calculateHOG(self.frame)
        path="/home/cristina/Documentos/TFG/ResultadosHOG/"+self.name()
        cv2.imwrite(path, self.HOGimage)


    def descriptorHOG(self):
        return self.hogStimate


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