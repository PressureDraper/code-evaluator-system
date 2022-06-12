import os
import pathlib

#Se define lo que se quiere esperar como resultado
esperado = """
.
└── renombrado.txt

0 directories, 1 file"""

#Código para analizar el entorno y comprobar si coincide con el resultado esperado
res = esperado.strip()

ruta = pathlib.Path(__file__).parent.absolute()

os.chdir(str(ruta) + '/' + 'testingfolder')

p = os.popen('tree').read().strip()

#Si coincide regresa 1 sino regresa 0
if res == p.strip():
    print(1)
else:
    print(0)