import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure
import numpy as np
from sklearn.cluster import KMeans

def calculateHOG(image):
    fd, hog_image=hog(image, orientation=8, pixels_per_cell=(16,16), cells_per_block=(1,1), visualize=True, multichannel=True)
    return exposure.rescale_intensity(hog_image, in_range=(0,10))


def kmeans(dataSet):
    print("Ejecutando kmeans")
    kmeans=KMeans(n_clusters=5, init='k-means++',random_state=42 )
    clusters=kmeans.fit_predict(dataSet)   
    return clusters