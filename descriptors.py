from skimage.feature import hog
import cv2
import csv
import os
import math
from frame import *
from utils import *
import statistics as stats


def checkOutIn(frame1, frame2, deb=False):
    d=distancia_euclidea(frame1.descriptorHOG(), frame2.descriptorHOG())
    if d>=9:
        c1=colorClass(frame1.imageColor())
        c2=colorClass(frame2.imageColor())
        if deb:
            print(c1, "   ", c2, " f1: ", frame1.name(), "f2: ", frame2.name())
        if (c2[0]=='R' and c2[1]>60) or (c1[0]!='R' and c2[0]=='R' and c2[1]>30):
            return True
        else:
            return False
    else:
        return False

def checkInOut(frame1, frame2, deb=False):
    d=distancia_euclidea(frame1.descriptorHOG(), frame2.descriptorHOG())
    if d>8.8:
        c1=colorClass(frame1.imageColor())
        c2=colorClass(frame2.imageColor())
        if deb:
            print(c1[0], "   ", c2[0], d)
        if c1[0]=='R' and c2[0]!='R':
            return True
        else:
            # if not checkColorInside(frame2.imageColor()):
            #     print(frame2.imageColor())
            #     return True
            # else:
            return False
    else:
        return False


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

