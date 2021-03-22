import cv2 




class frame():

    hogStimate=None

    def __init__(self, path, nFrame):
        self.path=path
        self.numeroFrame=nFrame
        self.frame=cv2.imread(path+str(nFrame)+".png")
        

    def calcularHOG(self):
        hog=cv2.HOGDescriptor()
        self.hogStimate=hog.compute(self.frame)
        print(self.hogStimate)
        
    def mostrarFrame(self):
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(0)
