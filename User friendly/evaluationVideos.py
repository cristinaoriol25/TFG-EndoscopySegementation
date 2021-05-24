from videoEndoscopy import videoEndoscopy
import os



def main():
    # path1="/home/cristina/Descargas/"
    # i=311
    # video="HCULB_00"+str(i)+"_procedure_thumbnail.webm"
    # v1=videoEndoscopy(path1, video, "HCULB_00"+str(i))
    # v1.toFrames("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/")
    # i=206
    # video="HCULB_00"+str(i)+"_procedure_thumbnail.webm"
    # v1=videoEndoscopy(path1, video, "HCULB_00"+str(i))
    # v1.toFrames("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/")
    # i=181
    # video="HCULB_00"+str(i)+"_procedure_thumbnail.webm"
    # v1=videoEndoscopy(path1, video, "HCULB_00"+str(i))
    # v1.toFrames("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/")
    # i=118
    # video="HCULB_00"+str(i)+"_procedure_thumbnail.webm"
    # v1=videoEndoscopy(path1, video, "HCULB_00"+str(i))
    # v1.toFrames("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/")
    # i="039"
    # video="HCULB_00"+str(i)+"_procedure_thumbnail.webm"
    # v1=videoEndoscopy(path1, video, "HCULB_00"+str(i))
    # v1.toFrames("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/")
    for carpeta in os.listdir("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/"):
        i=0
        for frame in sorted(os.listdir("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/"+carpeta+"/")):
            if i%10!=0: os.remove("/home/cristina/Documentos/TFG/Dataset/EvalutationLabels/"+carpeta+"/"+frame)
            i+=1

if __name__=='__main__':
    main()