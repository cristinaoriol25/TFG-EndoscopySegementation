import torch
import sys
import yaml
from torchvision import transforms, datasets
import torchvision
import numpy as np
import os
from torch.utils.data.dataloader import DataLoader
from videoDataset import *
sys.path.append('../')
from models.resnet_base_network import ResNet18
from data.transforms import get_simclr_data_transforms
from data.multi_view_data_injector import MultiViewDataInjector

def get_features_from_encoder(encoder, loader):
    
    x_train = []
    y_train = []

    # get the features from the pre-trained model
    print("get the features from the pre-trained model")
    for i, (x, y) in enumerate(loader):
        with torch.no_grad():
            feature_vector = encoder(x)
            x_train.extend(feature_vector)
            y_train.extend(y.numpy())
    print("Pre-atrined loaded")
    x_train = torch.stack(x_train)
    y_train = torch.tensor(y_train)
    return x_train, y_train


def main():
    batch_size = 512
    config = yaml.load(open("config/config.yaml", "r"), Loader=yaml.FullLoader)
    data_transforms = torchvision.transforms.Compose([transforms.ToTensor()])
    train_dataset=EndoscopyDataset("/workspace/coriol/ByolDataset/73-379/", transform=data_transforms)
    train_loader = DataLoader(train_dataset, batch_size=batch_size,
                          num_workers=0, drop_last=False, shuffle=True)
    device = 'cpu' #'cuda' if torch.cuda.is_available() else 'cpu'
    encoder = ResNet18(**config['network'])
    output_feature_dim = encoder.projetion.net[0].in_features
    #load pre-trained parameters
    load_params = torch.load(os.path.join('./model_segundaparte.pth'),
                            map_location=torch.device(torch.device(device)))

    if 'online_network_state_dict' in load_params:
        encoder.load_state_dict(load_params['online_network_state_dict'])
        print("Parameters successfully loaded.")

    #remove the projection head
    encoder = torch.nn.Sequential(*list(encoder.children())[:-1])    
    encoder = encoder.to(device)
    encoder.eval()
    x_train,y_train=get_features_from_encoder(encoder, train_loader)

    with open('features-Evaluation073-379.npy', 'wb') as f:
        np.save(f, np.array(x_train))
        np.save(f, np.array(train_dataset.getOrder()))
    




if __name__=='__main__':
    main()