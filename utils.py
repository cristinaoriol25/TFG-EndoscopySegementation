import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import cv2
import csv
import os
import statistics as stats

#BGR
def mediaColor(colores):
    b=[color[0] for color in colores]
    g=[color[1] for color in colores]
    r=[color[2] for color in colores]
    return [stats.mean(r), stats.mean(g), stats.mean(b)]

def medianaColor(colores):
    b=[color[0] for color in colores]
    g=[color[1] for color in colores]
    r=[color[2] for color in colores]
    return [stats.median(r), stats.median(g), stats.median(b)]


def filterClass(colores, valor, dominante):
    return [valor[i] for i in range(0, len(colores)) if colores[i]==dominante]

def dominante(colores):
    r=0
    g=0
    b=0
    for color in colores:
        if color=='R':
            r+=1
        elif color == 'G':
            g+=1
        else:
            b+=1
    if r>=g and r>=b:
        return 'R'
    elif g>=r and g>=b:
        return 'G'
    else:  
        return 'B'


def colorClass(color):
    if color[0] >= color[1] and color[0] >= color[2]:
        return 'B', color[0]
    elif color[0] <= color[1] and color[1] >= color[2]:
        return 'G', color[1]
    elif color[0] <= color[2] and color[2] >= color[1]:
        return 'R', color[2]

def indiceToName(i):
    i=str(i)
    name=i.rjust(6, "0")
    f=name+".png"
    return f

def renameFrames(path):
    for file in os.listdir(path):
        name=file
        name=name.split(".")
        name=name[0].rjust(6, "0")
        f=name+".png"
        os.rename(path+file, path+f)

def distancia_euclidea(a, b):
    return np.sqrt(sum((abs(a) - abs(b))**2))

def kmeans(dataSet):
    print("Ejecutando kmeans")
    kmeans=KMeans(n_clusters=2, init='k-means++',random_state=42 )
    clusters=kmeans.fit_predict(dataSet)   
    return clusters


def kmeansHOGCSV(path):
    #Usar esto para los tipos en el csv:
    #parse_dates = ['V1'] #specify the column you need for da
    #variables = pd.read_csv('date-dfki.csv', dtype={'V1': str, 'ip': np.str, 'n': np.int32}, parse_dates=parse_dates) #in data type you specify each column what format to use
    dataframe = pd.read_csv("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/framesFeatures.csv")
    X = np.array(dataframe["HOG"])
    kmeans = KMeans(n_clusters=5).fit(X)
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_
    print(centroids)
    with open('clusterHOG.csv', 'w') as csvfile:
        fieldnames = ['HOGCluster']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in labels:
            writer.writerow({'HOGCLuster':c})
