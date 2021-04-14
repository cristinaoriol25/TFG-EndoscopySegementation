#!/usr/bin/python
# -*- coding: UTF-8 -*-
from descriptors import *







def main():
    #calculateHogEstadistic("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Pruebas/Fuera/", "Fuera")
    #calculateHogEstadisticComparation("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Pruebas/Dentro/","/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Pruebas/Fuera/", "Comparación")
    calculateColorEstadistic("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Pruebas/Fuera/", "Fuera")
    calculateColorEstadistic("/home/cristina/Documentos/TFG/TFG-EndoscopySegementation/Pruebas/Dentro/", "Dentro")



if __name__ == "__main__":
    main()