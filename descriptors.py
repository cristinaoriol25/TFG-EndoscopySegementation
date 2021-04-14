from skimage.feature import hog
import cv2
import csv
import os
import math
from frame import *
from utils import *
import statistics as stats


def calculateHOG(image):
    fd, hog_image=hog(image, orientations=8, pixels_per_cell=(16,16), cells_per_block=(1,1), visualize=True, multichannel=True)
    return fd, exposure.rescale_intensity(hog_image, in_range=(0,10))

def calculateHogEstadistic(path, tipo):
    with open("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/estadisticHog.csv", 'a') as csvfile:
        fieldnames = ['Tipo','Media', 'Mediana', 'Mínimo', 'Máximo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        hog=[]
        i=0
        for file in os.listdir(path):
            f=frame(path, file)
            hog.append(f.descriptorHOG())
            # i+=1
            # if i>= 10: break
        statsH=[]
        indice=0
        while indice<len(hog)-1:
            statsH.append(distancia_euclidea(hog[indice], hog[indice+1]))
            indice+=1

        writer.writerow({'Tipo': tipo, 'Media': stats.mean(statsH), 'Mediana': stats.median(statsH), 'Mínimo': min(statsH), 'Máximo': max(statsH)})

def calculateHogEstadisticComparation(path1,path2, tipo):
    with open("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/estadisticHog.csv", 'a') as csvfile:
        fieldnames = ['Tipo','Media', 'Mediana', 'Mínimo', 'Máximo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        inside=os.listdir(path1)
        outside=os.listdir(path2)
        writer.writeheader()
        hog=[]
        i=0
        while i<len(inside) and i<len(outside):
            f1=frame(path1, inside[i])
            f2=frame(path2, outside[i])
            hog.append(distancia_euclidea(f1.descriptorHOG(), f2.descriptorHOG()))
            i+=1
        writer.writerow({'Tipo': tipo, 'Media': stats.mean(hog), 'Mediana': stats.median(hog), 'Mínimo': min(hog), 'Máximo': max(hog)})


def calculateColorEstadistic(path, tipo):
    with open("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/estadisticColor.csv", 'a') as csvfile:
        fieldnames = ['Tipo','Dominante','Media', 'Mediana']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        colorClase=[]
        color=[]
        i=0
        for file in os.listdir(path):
            f=frame(path, file)
            colorIm=f.imageColor()
            c, n=colorClass(colorIm)
            colorClase.append(c)
            color.append(colorIm)
            # i+=1
            # if i>= 10: break
        domin=dominante(colorClase)
        #color=filterClass(colorClase, color, domin)
        writer.writerow({'Tipo': tipo,'Dominante':domin, 'Media': mediaColor(color), 'Mediana': medianaColor(color)})

