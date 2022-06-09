import pathlib
import os
import re
import shutil

ruta = pathlib.Path(__file__).parent.absolute()

titulo = 'testing folder jeje'
titulo = titulo.lstrip()
title = re.sub(r"\s+", "", titulo)

if not os.path.exists(str(ruta) + '/' + title):
    os.makedirs(str(ruta) + '/' + title)

if os.path.exists(str(ruta) + '/' + title):
    os.chdir(str(ruta) + '/' + title)

file = open("filename.txt", "w")
file.write("Primera línea" + os.linesep)
file.write("Segunda línea")
file.close()

shutil.copy("filename.txt", "archivo.txt")

