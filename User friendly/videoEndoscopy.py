import frame
import ffmpeg
import os
import descriptors

class videoEndoscopy():
    def __init__(self, path, video, name):
        self.path=path
        self.video=video
        self.name=name
        self.frames=[]
        self.PathResult=None

    def setPathResult(self, path):
        self.PathResult=path

    def renameFrames(self, path):
        for file in os.listdir(path):
            name=file
            name=name.split(".")
            name=name[0].rjust(6, "0")
            f=name+".png"
            os.rename(path+file, path+f)

    def renameFramesRestart(self):
        files=os.listdir(self.PathResult+self.name+"/")
        files=sorted(files)
        i=0
        for file in files:
            name=str(i)
            name=name.rjust(6, "0")
            f=name+".png"
            os.rename(self.PathResult+self.name+"/"+file, self.PathResult+self.name+"/"+f)
            i+=1
    
    def toFrames(self, pathResult):
        self.PathResult=pathResult
        stream=ffmpeg.input(self.path+self.video)
        stream=ffmpeg.filter(stream, 'fps', fps=40, round = 'up')
        try:
            os.stat(pathResult+self.name+"/")

        except:
            os.mkdir(pathResult+self.name+"/")
        stream=ffmpeg.output(stream, pathResult+self.name+"/%d.png", video_bitrate='5000k',sws_flags='bilinear',start_number=0) 
        ffmpeg.run(stream)
        self.renameFrames(pathResult+self.name+"/")

    def searchEndoscopyIniEnd(self, pathResult=None):
        if len(self.frames)==0 and pathResult==None and self.PathResult==None:
            os.error("No hay path de resultados")
        elif len(self.frames)==0 and pathResult!=None:
            self.toFrames(pathResult)
        ini=-1
        fin=-1
        check=False
        checkRatio=0
        files =  os.listdir(self.PathResult+self.name+"/") #random order
        sorted_files =  sorted(files) #order by name
        indice=0
        stop=False
        print("Searching the start and the end from the video: ", self.name)
        while indice<len(sorted_files)-100 and not stop:
            if check:
                if ini != 1 and fin == -1:
                    f1=frame(self.PathResult+self.name+"/", frame.indiceToName(ini))
                    f2=frame(self.PathResult+self.name+"/", frame.indiceToName(indice))
                    if descriptors.checkOutIn(f1, f2, True):
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
                    f1=frame(self.PathResult+self.name+"/", frame.indiceToName(fin))
                    f2=frame(self.PathResult+self.name+"/", frame.indiceToName(indice))
                    if frame.checkInOut(f1,f2, True):
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
                f1=frame(self.PathResult+self.name+"/", frame.indiceToName(indice))
                f2=frame(self.PathResult+self.name+"/", frame.indiceToName(indice+10))
                if ini == -1 and fin == -1:
                    if descriptors.checkOutIn(f1,f2, True):
                        check=True
                        checkRatio+=1
                        ini=indice
                        checkRatio+=1
                elif ini != -1 and fin == -1:
                    if descriptors.checkInOut(f1, f2, True):
                        fin=indice
                        check=True
                        checkRatio+=1
                indice+=10
        print("Search ended, start frame: ", ini, " end frame: ", fin)
        if ini == -1 : ini=0
        if fin==-1 : fin=len(sorted_files)
        self.start=ini
        self.end=fin
        self.len=len(sorted_files)

    def getStart(self):
        if self.start is not None:
            return self.start
        else:
            os.error("Start not searched yet")
            exit
    def getEnd(self):
        if self.end is not None:
            return self.end
        else:
            os.error("End not searched yet")
            exit


    def cutVideo(self):
        i=0
        if self.start is not None:
            os.error("Start and end not searched yet")
            exit
        while i < self.start:
            os.remove(self.PathResult+self.name+"/"+frame.indiceToName(i))
            i+=1
        i=self.end+1
        while i <= len :
            try:
                os.remove(self.ResultPath+self.name+"/"+frame.indiceToName(i))
            except:
                pass
            i+=1
        self.renameFramesStart()

    def resultToVideo(self):
        os.system("ffmpeg -framerate 40  -i '"+self.ResultPath+self.name+"/"+"%6d.png' -vcodec h264 "+self.ResultPath+self.name+"/"+self.name+"_lossy.mov")
        os.system("ffmpeg -i "+self.ResultPath+self.name+"/"+self.name+"_lossy.mov -vcodec libvpx -qmin 0 -qmax 50 -crf 20 -b:v 200K  -s 320x240 "+self.ResultPath+self.name+"/"+self.name+"_thumbnail.mov")
        filelist= [file for file in os.listdir(self.ResultPath+self.name+"/") if file.endswith('.png')]
        for image in filelist:
            os.remove(self.ResultPath+self.name+"/"+image)

        
