from videoSegmentation import toFrames
import frame
import ffmpeg
import os
import utils

class videoEndoscopy():
    def __init__(self, path, videoName):
        self.path=path
        self.name=videoName
        self.frames=[]
        self.PathResult==None
    
    def toFrames(self, pathResult):
        self.PathResult=pathResult
        stream=ffmpeg.input(self.path+self.name)
        stream=ffmpeg.filter(stream, 'fps', fps=40, round = 'up')
        try:
            os.stat(pathResult+self.name+"/")

        except:
            os.mkdir(pathResult+self.name+"/")
        stream=ffmpeg.output(stream, pathResult+self.name+"/%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0) 
        ffmpeg.run(stream)
        utils.renameFrames(pathResult+self.name+"/")

    def searchEndoscopyIniEnd(self, pathResult=None):
        if len(self.frames)==0 and pathResult==None and self.PathResult==None:
            os.error("No hay path de resultados")
        elif len(self.frames)==0 and pathResult!=None:
            toFrames(pathResult)
        #VOY POR AQUI DE CAMBIAR
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
                    if checkOutIn(f1, f2, True):
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
                    if checkInOut(f1,f2, True):
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
                    if checkOutIn(f1,f2, True):
                        check=True
                        checkRatio+=1
                        ini=indice
                        checkRatio+=1
                elif ini != -1 and fin == -1:
                    if checkInOut(f1, f2, True):
                        fin=indice
                        check=True
                        checkRatio+=1
                indice+=10
            if indice%5000 == 0 : print("Frame analyzed: ", indice)
        print("Search ended, start frame: ", ini, " end frame: ", fin)
        if ini == -1 : ini=0
        if fin==-1 : fin=len(sorted_files)
        return ini, fin, len(sorted_files)
        
