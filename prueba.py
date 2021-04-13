#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import argparse
import os
import json
import csv
from frame import *
from utils import *
    
def main(args):
    f1=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Frames/video/", "000000.png")
    f2=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Frames/video/", "9800.png")
    f3=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Frames/video/", "10000.png")
    f4=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Frames/video/", "10200.png")
    f5=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Frames/video/", "10800.png")

    print("0-9800: ", distancia_euclidea(f1.descriptorHOG(), f2.descriptorHOG()))
    print("0-10000: ", distancia_euclidea(f1.descriptorHOG(), f3.descriptorHOG()))
    print("0-10200: ", distancia_euclidea(f1.descriptorHOG(), f4.descriptorHOG()))
    print("0-10800: ", distancia_euclidea(f1.descriptorHOG(), f5.descriptorHOG()))
    print("10000-10200: ", distancia_euclidea(f3.descriptorHOG(), f4.descriptorHOG()))
    print("10200-10800: ", distancia_euclidea(f4.descriptorHOG(), f5.descriptorHOG()))
    print("10000-10800: ", distancia_euclidea(f3.descriptorHOG(), f5.descriptorHOG()))





    





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    args = parser.parse_args()

    main(args)