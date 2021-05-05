import FilterModel
import cv2
import sys
import argparse

parser = argparse.ArgumentParser(description='Evaluate the video input_file and export the results on output_file')

parser.add_argument('input_file',type=str, help="Video input file path")
parser.add_argument('output_file',type=str,help="Output text file name")
parser.add_argument("--images_per_task",type=int,default=1,help="Number of frames processed at the same time")

FM = FilterModel.FilterModule()
args = parser.parse_args()

# input_file,output_file = sys.argv[1:]
# print(input_file)
# print(output_file)
with open(args.output_file,'w') as fp:
    cap = cv2.VideoCapture(args.input_file)
    frameNo=0
    end = False
    while 1:
        frames = []
        for i in range(args.images_per_task):
            ret,frame = cap.read()
            if frame is None:
                end = True
            frames.append(frame)
        if end:
            break
        Output = FM.process_multi(frames)
        for V in Output:
            fp.write(frameNo.__str__()+";"+V.__str__()+";\n")
            frameNo+=1
