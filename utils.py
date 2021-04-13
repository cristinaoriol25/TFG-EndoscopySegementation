import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import cv2
import csv
import os

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

def calculateHOG(image):
    fd, hog_image=hog(image, orientations=8, pixels_per_cell=(16,16), cells_per_block=(1,1), visualize=True, multichannel=True)
    return fd, exposure.rescale_intensity(hog_image, in_range=(0,10))

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
