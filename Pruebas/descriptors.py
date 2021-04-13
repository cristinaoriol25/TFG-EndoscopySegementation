#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import argparse
import ffmpeg
import os
import json
import csv
from frame import *
from utils import *

def calcularHOGFrames(path):
    #frames = [frame(path,archivo) for archivo in os.listdir(path)]#os.listdir(ejemplo_dir)
    #descr= dict((f, f.descripHOG()) for f in [frame(path,archivo) for archivo in os.listdir(path)])
    print("Calculando HOG")
    files =  os.listdir(path) #random order
    sorted_files =  sorted(files) #order by name
    #descr=[f.descripHOG() for f in frames]
    with open('framesFeatures.csv', 'w') as csvfile:
        fieldnames = ['Frame', 'HOG']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for f in sorted_files:
            writer.writerow({'Frame': f, 'HOG': descripHOG(path, f)})
    print("Calculado HOG")


def calcularKmeansColorDominante(path):
    color=[]
    frames=[]
    files =  os.listdir(path) #random order
    sorted_files =  sorted(files) #order by name
    for file in sorted_files:  
        f=frame(path, file)
        color.append(f.imageColor())
        frames.append(f)
    label=kmeans(color)
    indice=0
    for c in label:
        path="/home/cristina/Documentos/TFG/Resultados/Color/cluster"+str(c)+"/"
        try:
            os.stat(path)
        except:
            os.mkdir(path)
        frames[indice].guardarFrame(path)
        indice+=1


def clusterHOG(path):
    #calcularHOGFrames(path)
    kmeansHOGCSV(path)
    # cl=kmeans(data)
    # i=0
    # dic={}
    # for frame in frames:
    #     dic[frame]=cl[i]
    #     i=i+1
    # print(dic)

def saveHOG(path):
    hog=[]
    frames=[]
    files =  os.listdir(path) #random order
    sorted_files =  sorted(files) #order by name
    for file in sorted_files:  
        f=frame(path, file)
        f.imageHOG()
        hog.append(f.descriptorHOG())
        frames.append(f)
    label=kmeans(hog)
    
    with open('clusterHOG.csv', 'w') as csvfile:
        fieldnames = ['Frame','Cluster']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   
        writer.writeheader()
        indice=0
        for c in label:
            writer.writerow({'Frame':frames[indice].name(),'Cluster':c})
            path="/home/cristina/Documentos/TFG/Resultados/HOG/cluster"+str(c)+"/"
            try:
                os.stat(path)
            except:
                os.mkdir(path)
            frames[indice].guardarFrame(path)
            indice+=1


def renameFrames(path):
    for file in os.listdir(path):
        name=file
        name=name.split(".")
        name=name[0].rjust(6, "0")
        f=name+".png"
        os.rename(path+file, path+f)
    


def main(args):
    video="video.webm"
    vName=video.split(".")
    try:
        os.stat("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Frames/"+vName[0]+"/")
    except:
        os.mkdir("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Frames/"+vName[0]+"/")
        stream=ffmpeg.input(video)
        stream=ffmpeg.filter(stream, 'fps', fps=40, round = 'up')
        stream=ffmpeg.output(stream, "/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Frames/"+vName[0]+"/%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0)
        ffmpeg.run(stream)
        renameFrames("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Frames/"+vName[0]+"/")
    frames=sorted(os.listdir("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Frames/"+vName[0]+"/"))
    descriptor=np.empty((len(frames), 3))
    vName=video.split(".")
    for file in frames:
        name=file.split(".")
        f=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Frames/"+vName[0]+"/", file)
        descriptor[int(name[0])][0]=name[0]
        print(type(f.descriptorHOG().ravel()))
        descriptor[int(name[0])][1]=f.descriptorHOG()
        descriptor[int(name[0])][2]=f.imageColor()
    print(descriptor)
    try:
        os.stat("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+vName[0]+"Descriptors")
    except:
        os.mkdir("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+vName[0]+"Descriptors")    
    np.save("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+vName[0]+"Descriptors", descriptor)
    ##TODO: CAMBIAR A CSV
    

    





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)