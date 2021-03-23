#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import argparse
import ffmpeg
import os
import json
from frame import *
from utils import *

def readFrameFromJson(jsonFile):
    with open(jsonFile, 'r') as f:
            dict = {}
            content = f.read()
            f_dict = json.loads(content)
            dict['stimated frame to cut']=f_dict['stimated frame to cut'] #Este campo del diccionario lo reemplazarías por tu campo texto
            return dict['stimated frame to cut']

def cutVideo(path, json):
    #totalFrames=len(glob.glob("path/*.png"))
    firstFrame=int(readFrameFromJson(json))
    #print(firstFrame)
    toRemove=list(range(0, firstFrame))
    for i in toRemove:
        frame = path+str(i) +".png"    
        os.remove(frame)

def calcularHOGFrames(path):
    #frames = [frame(path,archivo) for archivo in os.listdir(path)]#os.listdir(ejemplo_dir)
    #descr= dict((f, f.descripHOG()) for f in [frame(path,archivo) for archivo in os.listdir(path)])
    print("Calculando HOG")
    frames=[frame(path,archivo) for archivo in os.listdir(path)]
    descr=[f.descripHOG() for f in frames]
    return frames, descr



def clusterHOG(path):
    frames,data=calcularHOGFrames(path)
    cl=kmeans(data)
    i=0
    dic={}
    for frame in frames:
        dic[frame]=cl[i]
        i=i+1
    print(dic)


def main(args):
    if args.video is not None:
        stream=ffmpeg.input(args.video)
        stream=ffmpeg.filter(stream, 'fps', fps=40, round = 'up')
        stream=ffmpeg.output(stream, "/home/pazagra/Cris/Frames/prueba-%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0)
        ffmpeg.run(stream)
    if args.videoFrames is not None:
        pathFrames=args.videoFrames 
        if args.json is not None:
            jsonPath=args.json
            cutVideo(pathFrames, jsonPath)
    if args.pathH is not None:
        clusterHOG(args.pathH)





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--video", help="Convert video to frames",
                        type=str, default=None)
    parser.add_argument("-s", "--videoFrames", help="Cut the video on the indicated frame on the json",
                        type=str, default=None)
    parser.add_argument("-j", "--json", help="Json from the indicated video",
                        type=str, default=None)
    parser.add_argument("-hg", "--pathH", help="HOG from the indicated video",
                        type=str, default=None)
    
    args = parser.parse_args()

    main(args)