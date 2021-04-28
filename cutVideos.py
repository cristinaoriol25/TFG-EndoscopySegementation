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
from descriptors import *


def segmentate(path, video, resultPath):
    """
    Transform a video into frames and calculates the hog stimate for each 10 frames searching the start and the end point of the  medical procedure
    """
    toFrames(path, video, resultPath)
    ini=-1
    fin=-1
    check=False
    checkRatio=0
    renameFrames(resultPath)
    files =  os.listdir(resultPath) #random order
    sorted_files =  sorted(files) #order by name
    indice=0
    stop=False
    print("Searching the start and the end from the video: ", video)
    while indice<len(sorted_files)-100 and not stop:
        if check:
            if ini != 1 and fin == -1:
                
                f1=frame(resultPath, indiceToName(ini))
                f2=frame(resultPath, indiceToName(indice))
                if checkOutIn(f1, f2):
                    if checkRatio <= 5:
                        checkRatio+=1
                    else:
                        checkRatio=0
                        check=False
                        print("Inicio encontrado: ", ini)
                    indice+=10
                else:
                    check=False
                    checkRatio=0
                    ini=-1
            if ini != 1 and fin != -1:
                
                f1=frame(resultPath, indiceToName(fin))
                f2=frame(resultPath, indiceToName(indice))
                if checkInOut(f1,f2):
                    if checkRatio <= 5:
                        checkRatio+=1
                    else:
                        checkRatio=0
                        check=False
                        stop=True
                    indice+=10
                else:
                    check=False
                    checkRatio=0
                    fin=-1
        else:
            
            f1=frame(resultPath, indiceToName(indice))
            f2=frame(resultPath, indiceToName(indice+10))
            if ini == -1 and fin == -1:
                if checkOutIn(f1,f2):
                    check=True
                    checkRatio+=1
                    ini=indice
                    checkRatio+=1
            elif ini != -1 and fin == -1:
                if checkInOut(f1, f2):
                    fin=indice
                    check=True
                    checkRatio+=1
            indice+=10
        if indice%5000 == 0 : print("Frame analyzed: ", indice)
    print("Search ended, start frame: ", ini, " end frame: ", fin)
    if ini == -1 : ini=0
    if fin==-1 : fin=len(sorted_files)
    return ini, fin, len(sorted_files)


def removeFrames(start, end, len, video, resultPath):
    i=0
    while i < start:
        os.remove(resultPath+indiceToName(i))
        i+=1
    i=end
    while i <= len :
        try:
            os.remove(resultPath+indiceToName(i))
        except:
            print("Incorrect ",i)
        i+=1

def removeAllFrames(start, end, video, resultPath):
    i=start 
    while i<=end :
        try:
            os.remove(resultPath+indiceToName(i))
        except:
            print("Incorrect ",i)
        i+=1




def toVideo(path, video):
    os.system("ffmpeg -framerate 40  -i '"+path+"%6d.png' -vcodec h264 "+path+video+".mov")
    os.system("ffmpeg -i "+path+video+".mov -vcodec libvpx -qmin 0 -qmax 50 -crf 20 -b:v 200K  -s 320x240 "+path+video)

def toFrames(path, video, resultPath):
    stream=ffmpeg.input(path+video)
    stream=ffmpeg.filter(stream, 'fps', fps=40, round = 'up')
    try:
        os.stat(resultPath)

    except:
        os.mkdir(resultPath)
    stream=ffmpeg.output(stream, resultPath+"%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0) 
    ffmpeg.run(stream)
    
def main(args):
    if args.segmentation is not None and args.video is not None and args.result is not None:

        start, end, len=segmentate(args.segmentation, args.video, args.result)
        removeFrames(start, end, len, args.video, args.result)
        renameFramesRestart(args.result)
        toVideo(args.result, args.video)
        removeAllFrames(0, end-start, args.video, args.result)
    else:
        print("Incorrect parameters: python cutVideos.py -p 'path to the video/' -v 'name of the video' -r 'path to the result folder/'  ,the path to the video must be the path from the folder with the final '/' but not adding the name of the video, the path to the result must be a non existing folder, the program will create it, or an empty one")
        

        


    





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", help="video to segmentate",
                        type=str, default=None)
    parser.add_argument("-p", "--segmentation", help="Path from the video",
                        type=str, default=None)
    parser.add_argument("-r", "--result", help="Path from the result video",
                        type=str, default=None)
    
    args = parser.parse_args()

    main(args)