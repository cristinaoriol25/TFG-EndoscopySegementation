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


def segmentate(path, video):
    """
    Transform a video into frames and calculates the hog stimate for each 10 frames searching the start and the end point of the  medical procedure
    """
    toFrames(path, video)
    ini=-1
    fin=-1
    check=False
    checkRatio=0
    #renameFrames("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/")
    renameFrames("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/")
    #files =  os.listdir("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/") #random order
    files =  os.listdir("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/") #random order
    sorted_files =  sorted(files) #order by name
    indice=0
    stop=False
    print("Searching the start and the end from the video: ", video)
    while indice<len(sorted_files)-100 and not stop:
        if check:
            if ini != 1 and fin == -1:
                # f1=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(ini))
                # f2=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice+10))
                f1=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(ini))
                f2=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice))
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
                # f1=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(fin))
                # f2=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice+10))
                f1=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(fin))
                f2=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice))
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
            # f1=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice))
            # f2=frame("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice+10))
            f1=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice))
            f2=frame("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/", indiceToName(indice+10))
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
    if fin==-1 : fin=len(sorted_files)-100
    return ini, fin, len(sorted_files)


def removeFrames(start, end, len, video):
    i=0
    while i < start:
        # os.remove("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/"+indiceToName(i))
        os.remove("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/"+indiceToName(i))
        i+=1
    i=end
    while i < len :
        # os.remove("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/"+indiceToName(i))
        os.remove("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/"+indiceToName(i))
        i+=1

def removeAllFrames(start, end, video):
    i=start 
    while i<=end :
        # os.remove("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/"+indiceToName(i))
        try:
            os.remove("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/"+indiceToName(i))
        except:
            print("Indice ",i)
        i+=1

def readFrameFromJson(jsonFile): 
    """
    Read the stimated cut from the json file
    """ 
    with open(jsonFile, 'r') as f:
            dict = {}
            content = f.read()
            f_dict = json.loads(content)
            dict['stimated frame to cut']=f_dict['stimated frame to cut'] 
            return dict['stimated frame to cut']


def cutVideo(path, json):   
    """
    Cut the video on the frame indicated by the json file
    """ 
    firstFrame=int(readFrameFromJson(json))
    toRemove=list(range(0, firstFrame))
    for i in toRemove:
        frame = path+str(i) +".png"    
        os.remove(frame)

# def toVideo(path, video):
#     # stream=ffmpeg.input("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/*.png")
#     # #stream=ffmpeg.output(stream, "/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/"+video+"Segementation.webm")
#     # stream=ffmpeg.output(stream, "/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/"+video+"Segementation.webm")
#     # ffmpeg.run(stream)
#     files=sorted(os.listdir('/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/'+video+'/'))
#     (
#     ffmpeg
#     .input(files, pattern_type='glob', framerate=40)
#     .filter(stream, 'fps', fps=40, round = 'up')
#     .output('movie.webm', crf=20, preset='slower', movflags='faststart', pix_fmt='yuv420p')
#     .view(filename='filter_graph')
#     .run()
#     )

def toVideo(path, video):
    os.system("cd "+path)
    os.system("ffmpeg -framerate 40 -start_number 002700 -i '"+path+"%6d.png' -vcodec h264 "+path+video+".mov")
    os.system("ffmpeg -i "+path+video+".mov -vcodec libvpx -qmin 0 -qmax 50 -crf 20 -b:v 200K  -s 320x240 "+path+video+".webm")

def toFrames(path, video):
    stream=ffmpeg.input(path+video)
    stream=ffmpeg.filter(stream, 'fps', fps=40, round = 'up')
    try:
        #os.stat("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/")
        os.stat("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/")

    except:
        #os.mkdir("/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/")
        os.mkdir("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/")
    #stream=ffmpeg.output(stream, "/home/pazagra/Cris/TFG-EndoscopySegementation/Results/"+video+"/%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0)
    stream=ffmpeg.output(stream, "/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+video+"/%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0) 
    ffmpeg.run(stream)
    
def main(args):
    if args.path is not None and args.video is not None:
        toFrames(args.path, args.video)
    if args.videoFrames is not None:
        pathFrames=args.videoFrames 
        if args.json is not None:
            jsonPath=args.json
            cutVideo(pathFrames, jsonPath)
    if args.segmentation is not None and args.video is not None:
        # start, end, len=segmentate(args.segmentation, args.video)
        # removeFrames(start, end, len, args.video)
        #renameFramesRestart('/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/'+args.video+'/')
        toVideo("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Results/"+args.video+"/", args.video)
        


    





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--path", help="Convert video to frames from path",
                        type=str, default=None)
    parser.add_argument("-v", "--video", help="video to segmentate",
                        type=str, default=None)
    parser.add_argument("-s", "--videoFrames", help="Cut the video on the indicated frame on the json",
                        type=str, default=None)
    parser.add_argument("-j", "--json", help="Json from the indicated video",
                        type=str, default=None)
    parser.add_argument("-sG", "--segmentation", help="Path from the video",
                        type=str, default=None)
    parser.add_argument("-vR", "--result", help="If True the result of the segmentation is a video, if False frames",
                        type=bool, default=False)
    
    args = parser.parse_args()

    main(args)