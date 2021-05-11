#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np


def main():
    cam=cv2.VideoCapture(0)
    if cam.isOpened():
        _,frame=cam.read()
        cv2.imwrite("original.txt)", frame)
        frame2=np.float32(frame.reshape(-1,3))
        cv2.imwrite("res.png)", frame2)






    





if __name__ == "__main__":

    main()