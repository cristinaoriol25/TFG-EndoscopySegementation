import cv2
import numpy as np
import torch
from torch.utils.data import Dataset,get_worker_info
from torchvision import transforms

from PIL import Image
inputp="/workspace/pazagra/Dataset/"
labels = {'rectum':0,'sigmoid':1,'descending':2,'esplenic':3,'transverse':4,
          'hepatic':5,'ascending':6,'ileocecal':7,'ileum':8,'cecum':9}

def expand_greyscale(t):
    return t.expand(3, -1, -1)

class VideoFrame():
    def __init__(self,sequence,number,label=None,fil=None):
        self.sequence=sequence
        self.number=number
        self.fil=fil
        self.label=label
        self.img = None

    def setLabel(self,label):
        self.label = label
    def getlabel(self):
        return self.label

    def setFil(self,fil):
        self.fil = fil
    def getFil(self):
        return self.fil

    def setimg(self,img):
        self.img = img
    def getimg(self):
        return self.img


class VideoDataset(Dataset):
    def __init__(self, sequences, image_size,mode):
        super().__init__()
        self.sequences = sequences
        self.imgs=[]
        self.cap = np.zeros((10),dtype=np.float32)
        self.last_seq = None
        for seq in self.sequences:
            with open(inputp+seq+".txt",'r') as fp:
                lines = fp.readlines()
            for l in lines:
                data=l.split(";")
                s = data[0]
                n=int(data[1])
                label=None
                fil=None
                if len(data)>=3:
                    label=data[2]
                if len(data)>=4:
                    fil=data[3]=='tensor(True)'
                vimg =VideoFrame(s,n,label,fil)
                if n==0:
                    continue
                if mode and not fil:
                    continue
                self.cap[labels[label]]+=1
                self.imgs.append(vimg)
            # self.cap[seq] = []
            # for i in range(6):
            #     self.cap[seq].append(cv2.VideoCapture(inputp+i.__str__()+"/" + seq + ".mov"))
        print(f'{len(self.imgs)} images found')

        self.transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Lambda(expand_greyscale)
        ])

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        def genlab(s,n):
            lab = np.zeros(n,dtype=np.float32)
            if s == True:
                lab[1]=1.0
            elif s==False:
                lab[0]=1.0
            else:
                lab[labels[s]]=1.0
            return lab
        img = self.imgs[index]
        # print(inputp+img.sequence+"/07"+img.number.__str__()+".png")
        img_d =cv2.imread(inputp+img.sequence+"/07"+img.number.__str__()+".png")
        # print(img_d.shape)
        img_d = cv2.cvtColor(img_d, cv2.COLOR_BGR2RGB)
        # print(img_d.shape,flush=True)
        image = Image.fromarray(img_d)
        # print(img.label,flush=True)
        return self.transform(image),torch.tensor(genlab(img.label,10)),torch.tensor(genlab(img.fil,2))

    def get_weight(self):
        # mini = min(self.cap)
        avg = sum(self.cap)
        # weights1 = np.reciprocal(self.cap/mini)
        weights2 = np.reciprocal(self.cap/avg)
        return torch.tensor(weights2)

    def dump_dataset(self,file):
        with open(inputp+file,'w') as fp:
            for data in self.imgs:
                line = data.sequence+";"+data.number.__str__()+";"+data.label+";"+data.fil.__str__()+";\n"
                fp.write(line)
