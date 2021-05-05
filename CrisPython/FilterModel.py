from PIL import Image
import torch
import cv2
from torch import nn
from torchvision import models, transforms
from byol_pytorch import BYOL
import pytorch_lightning as pl

resnet = models.resnet50(pretrained=False)

class SelfSupervisedLearner(pl.LightningModule):
    def __init__(self, net, **kwargs):
        super().__init__()
        self.learner = BYOL(net, **kwargs)
        self.last = nn.Sequential(
        nn.Linear(1000, 2),
        nn.Softmax(dim=1))

    def forward(self, images):
        x= self.learner.net(images)
        return self.last(x)


def expand_tensor(t):
    return t.expand(3, -1, -1)

class FilterModule():
    def __init__(self):
        self.model = SelfSupervisedLearner(
            resnet,
            image_size=256,
            hidden_layer='avgpool',
            projection_size=256,
            projection_hidden_size=4096,
            moving_average_decay=0.99
        )
        checkpoint = torch.load("FilterModel.ckpt")
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.eval()
        self.transform = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(256),
                    transforms.ToTensor(),
                    transforms.Lambda(expand_tensor)
                ])
    def process_one(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        input = self.transform(image).unsqueeze(0)
        out = self.model.forward(input)[0]
        if out[1]>=0.5:
            return True
        else:
            return False

    def process_already(self,imgs):
        input = torch.cat(imgs, 0)
        out = self.model.forward(input)
        outputs = []
        for i in range(len(imgs)):
            outputs.append(out[i][1] >= 0.5)
        return outputs

    def process_multi(self,images):
        img_trans=[]
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img)
            input = self.transform(image).unsqueeze(0)
            img_trans.append(input)
        input = torch.cat(img_trans,0)
        out = self.model.forward(input)
        outputs=[]
        for i in range(len(images)):
            outputs.append(out[i][1]>=0.5)
        return outputs