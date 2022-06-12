import os
import sys
import pathlib

param1 = sys.argv[1]
param2 = sys.argv[2]

ruta = pathlib.Path(__file__).parent.absolute()

os.chdir(str(ruta) + '/' + 'testingfolder')
os.remove(param1)

os.rename('filename.txt', param2)

file = open(param2, 'r')
txt = file.read()
print(txt)