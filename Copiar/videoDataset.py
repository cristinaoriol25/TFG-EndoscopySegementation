from __future__ import print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from PIL import Image

import warnings
warnings.filterwarnings("ignore")


class Frame():
    def __init__(self,path,sequence,number):
        self.path=path
        self.sequence=sequence
        self.number=number
        self.img = None
        self.label="0"

    def getSequence(self):
        return self.sequence
    def getNumber(self):
        return self.number
    def getLabel(self):
        return self.label
    def getFrame(self):
        return self.setFrame()
    def setFrame(self):
        # self.img=cv2.imread(self.path+"self.sequence/"+str(self.number).rjust(6,"0")+".png")
        return Image.open(self.path+self.sequence+"/"+str(self.number).rjust(6,"0")+".png")
    def printFrame(self):
        return  self.getSequence()+":"+self.getNumber()

class EndoscopyDataset(Dataset):   #Tranform-> leer con opencv.. to tensor
    def __init__(self,path, transform=None):
        super().__init__()
        self.imgs=[]
        self.path=path
        self.trans=transform
        self.order=[]
        for seq in sorted(os.listdir(path)):
            if os.path.isdir(path+seq):
                for img in sorted(os.listdir(path+seq+"/")):
                    if os.path.isfile(path+seq+"/"+img):
                        img=img.split(".")
                        f=Frame(path,seq, img[0])
                        self.imgs.append(f)   
        print(f'{len(self.imgs)} images found')
        self.transform = transforms.Compose([
            # transforms.Resize(image_size),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        frame=self.imgs[index]
        self.order.append(frame.printFrame())
        frame=self.trans(frame.getFrame())
        return frame, np.array((0))

    def getOrder(self):
        return self.order

    