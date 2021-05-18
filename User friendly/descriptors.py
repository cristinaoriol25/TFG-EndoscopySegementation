from frame import *
import statistics as stats


def distancia_euclidea(a, b):
    return np.sqrt(sum((abs(a) - abs(b))**2))

#BGR
def mediaColor(colores):
    b=[color[0] for color in colores]
    g=[color[1] for color in colores]
    r=[color[2] for color in colores]
    return [stats.mean(r), stats.mean(g), stats.mean(b)]

def medianaColor(colores):
    b=[color[0] for color in colores]
    g=[color[1] for color in colores]
    r=[color[2] for color in colores]
    return [stats.median(r), stats.median(g), stats.median(b)]


def filterClass(colores, valor, dominante):
    return [valor[i] for i in range(0, len(colores)) if colores[i]==dominante]

def dominante(colores):
    r=0
    g=0
    b=0
    for color in colores:
        if color=='R':
            r+=1
        elif color == 'G':
            g+=1
        else:
            b+=1
    if r>=g and r>=b:
        return 'R'
    elif g>=r and g>=b:
        return 'G'
    else:  
        return 'B'

def checkColorInside(color):
    return color[0]>30 and color[1]>60 and color[2]>100


def colorClass(color):
    if color[0] >= color[1] and color[0] >= color[2]:
        return 'B', color[0]
    elif color[0] <= color[1] and color[1] >= color[2]:
        return 'G', color[1]
    elif color[0] <= color[2] and color[2] >= color[1]:
        return 'R', color[2]

def checkOutIn(frame1, frame2, deb=False):
    d=distancia_euclidea(frame1.descriptorHOG(), frame2.descriptorHOG())
    if d>=9:
        c1=colorClass(frame1.imageColor())
        c2=colorClass(frame2.imageColor())
        if deb:
            print(c1, "   ", c2, " f1: ", frame1.name(), "f2: ", frame2.name())
        if (c2[0]=='R' and c2[1]>60) or (c1[0]!='R' and c2[0]=='R' and c2[1]>30):
            return True
        else:
            return False
    else:
        return False

def checkInOut(frame1, frame2, deb=False):
    d=distancia_euclidea(frame1.descriptorHOG(), frame2.descriptorHOG())
    if d>8.8:
        c1=colorClass(frame1.imageColor())
        c2=colorClass(frame2.imageColor())
        if deb:
            print(c1[0], "   ", c2[0], d)
        if c1[0]=='R' and c2[0]!='R':
            return True
        else:
            # if not checkColorInside(frame2.imageColor()):
            #     print(frame2.imageColor())
            #     return True
            # else:
            return False
    else:
        return False


