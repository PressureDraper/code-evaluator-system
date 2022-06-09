import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from modelo import models
from django.http import JsonResponse
from django.core.mail import send_mail
import datetime
import hashlib
import shutil
from pathlib import Path
import os
import time
import re

redirectLogin = '/login'
BASE_DIR = Path(__file__).resolve().parent.parent

def send_email(user, email, passwd):
    tdate = datetime.datetime.now() #tdate becomes an object so we can use attributes
    date = tdate.strftime("%d/%m/%Y | %H:%M") #Personalize a date time
    message = f"""
Fecha: {date}\n
Usuario: {user}\n
Email: {email}\n
Contraseña: {passwd}
        """
    try:
        send_mail(
            'Confirmación de Registro Sistema Evaluador',
            message,
            'rojeru.san1983@gmail.com',
            [f'{email}'],
            fail_silently=False,
        )
        return redirect(redirectLogin)
    except Exception as e:
        raise RuntimeError(f'No se ha podido enviar el Email correspondiente: {e}')

def logout(request):
    request.session['cookie_session'] = False
    return redirect(redirectLogin)

def valida_email(email, role):
    lista = []
    try:
        partes = email.split('@')
        if partes[1] == 'estudiantes.uv.mx' or partes[1] == 'uv.mx':
            if partes[1] == 'estudiantes.uv.mx' and role == 'estudiante' or partes[1] == 'uv.mx' and role == 'maestro':
                lista.append(partes[1])
                lista.append(True)
                return lista
            else:
                lista.append(partes[1])
                lista.append(False)
                return lista
        else:
            lista.append(partes[1])
            lista.append(False)
            return lista
    except Exception as e:
        raise RuntimeError(f'Ha ocurrido un error al verificar el Email: {e}.')

def valida_password(passwd):
    mayusculas = 0
    minusculas = 0
    numeros = 0
    digitos = 0
    caracteres = '*$&-/!#'
    if len(passwd) > 8:
        for letra in passwd:
            if letra.upper():
                mayusculas = 1

        for letra in passwd:
            if letra.lower():
                minusculas = 1

        for num in passwd:
            if num.isnumeric() == True:
                numeros = 1

        for dig in caracteres:
            if dig in passwd:
                digitos = 1
        
        if mayusculas == 1 and minusculas == 1 and numeros == 1 and digitos == 1:
            return True
        else:
            return False
    else:
        return False

def hashear(passwd):
    hasher = hashlib.sha256()
    binary = passwd.encode('utf-8')
    hasher.update(binary) 
    binhash = hasher.hexdigest() #bytes hash

    return binhash

def identificar(user):
    if user.startswith("zs"):
        return True
    else:
        return False

def get_usuario(email):
    partes = email.split('@')
    return partes[0].lower()

def post_enviar(usuario, user, passwd):
    if usuario == True:
        print(f'{user} es Alumno')
        if models.alumnos.objects.get(usuario = user):
            #obtener el objeto completo de la consulta
            obj = models.alumnos.objects.get(usuario = user)
            #comparar valores del input con los de la base de datos
            if user.lower() == obj.usuario.lower() and passwd.lower() == obj.passwd.lower():
                #Se crea la cookie de sesion recuperando un dato
                return {'valor': 1, 'usuario': 'alumno'}
            else:
                return {'valor': 0, 'usuario': 'alumno'}
        else:
            print(f'El usuario {usuario} no se encuentra en la base de datos.')
            return redirect(redirectLogin)
    else:
        print(f'{user} es Maestro')
        if models.maestros.objects.get(usuario = user):
            #obtener el objeto completo de la consulta
            obj = models.maestros.objects.get(usuario = user)
            #comparar valores del input con los de la base de datos
            if user.lower() == obj.usuario.lower() and passwd.lower() == obj.passwd.lower():
                #Se crea la cookie de sesion recuperando un dato
                return {'valor': 1, 'usuario': 'maestro'}
            else:
                return redirect(redirectLogin)
        else:
            print(f'El usuario {usuario} no se encuentra en la base de datos.')
            return redirect(redirectLogin)

def post_registrar(a, b, email, passwd):
    if a[1] == True and b == True:
        user = get_usuario(email)
        if a[0] == "uv.mx":
            #Si es maestro lo guardamos en tabla de maestros
            passwdh = hashear(passwd)
            try:
                obj = models.maestros(
                    usuario=user, 
                    email=email,
                    passwd=passwdh
                )
                obj.save()
                # send_email(user, email, passwd)
            except Exception as e:
                return e
        elif a[0] == "estudiantes.uv.mx":
            #Si es alumno lo guardamos en tabla de aliumnos
            passwdh = hashear(passwd)
            try:
                obj = models.alumnos(
                    usuario=user, 
                    email=email,
                    passwd=passwdh
                )
                obj.save()
                # send_email(user, email, passwd)
            except Exception as e:
                return e
        context = {'valor': 0}
        return context
    else:
        context = {'valor': 1}
        return context

def login(request):
    x = 'login.html'
    if request.method == 'GET':
        return render(request, x, {})
    if request.method == 'POST':
        if request.POST.get('enviar'):
            #obtener los valores de user y passwd de los inputs
            user = request.POST.get('user')
            passwd = request.POST.get('passwd')

            #Convertir la contraseña a su respectivo hash para verificar con el hash almacenado en la base de datos
            passwd = hashear(passwd)
            try:
                usuario = identificar(user.lower())
                respuesta = post_enviar(usuario, user, passwd)
                if respuesta['valor'] == 1 and respuesta['usuario'] == 'alumno':
                    #Se crea la cookie de sesion recuperando un dato
                    request.session['cookie_session'] = request.POST.get('user', '')
                    return redirect('/alumno')
                elif respuesta['valor'] == 1 and respuesta['usuario'] == 'maestro':
                    #Se crea la cookie de sesion recuperando un dato
                    request.session['cookie_session'] = request.POST.get('user', '')
                    return redirect('/docente')
                else:
                    return redirect(redirectLogin)
            except:
                return redirect(redirectLogin)
        elif request.POST.get('registrar'):
            email = request.POST.get('email')
            role = request.POST.get('role')
            passwd = request.POST.get('passwd')
            a = valida_email(email.lower(), role.lower())
            b = valida_password(passwd)
            respuesta = post_registrar(a, b, email, passwd)
            try:
                if respuesta['valor'] == 0:
                    return render(request, x, respuesta)
                elif respuesta['valor'] == 1:
                    return render(request, x, {'valor': 1})
            except Exception as e:
                print(e)
                return render(request, x, {'valor': 1})

def page4(request):
    t = 'welcome.html'
    #Se guarda la información de la cookie de sesión
    data = request.session.get('cookie_session', '')
    if data:
        return render(request, t, {'name': data})
    else:
        return redirect(redirectLogin)

def maestros(request):
    t = 'maestros.html'
    data = request.session.get('cookie_session', '')
    if data:
        return render(request, t, {'name': data})
    else:
        return redirect(redirectLogin)

def alumnos(request):
    template = 'alumnos.html'
    data = request.session.get('cookie_session', '')
    if request.method == 'GET':
        if data:
            obj = models.alumnos.objects.get(usuario = data)
            if obj.nombre == '':
                return render(request, template, {'name': data, 'setname': 1})
            else:
                return render(request, template, {'name': data, 'setname': 0})
        else:
            return redirect(redirectLogin)
    if request.method == 'POST':
        obj = models.alumnos.objects.get(usuario = data)
        nombre = request.POST.get('setName')
        obj.nombre = nombre
        obj.save()
        return redirect('/perfil')

# @csrf_exempt
def mostrar_alumnos(request):
    template = 'mostrarAlumnos.html'
    data = request.session.get('cookie_session', '')
    alumnos = models.alumnos.objects.filter(idMaestro = None)
    if request.method == 'GET':
        if data:
            return render(request, template, {'name': data, 'alumnos': alumnos})
        else:
            return redirect(redirectLogin)
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        maestro = models.maestros.objects.get(usuario = data)
        for aidi in jsondata:
            alumno = models.alumnos.objects.get(id = aidi['aidi'])
            alumno.idMaestro = maestro
            alumno.save()
        
        return redirect('/grupo')

def mostrar_perfil(request):
    template = 'mostrarPerfil.html'
    data = request.session.get('cookie_session', '')
    if request.method == 'GET':
        if data:
            user = identificar(data.lower())
            print(user)
            if user == True: #Si es alumno
                obj = models.alumnos.objects.get(usuario = data)
                nombre = obj.nombre
                correo = obj.email
                return render(request, template, {'nombre': nombre, 'correo': correo, 'usuario': 'alumno'})
            elif user == False: #Si es maestro
                obj = models.maestros.objects.get(usuario = data)
                nombre = obj.usuario
                correo = obj.email
                return render(request, template, {'nombre': nombre, 'correo': correo, 'usuario': 'maestro'})
        else:
            return redirect(redirectLogin)

def mostrar_grupo(request):
    template = 'mostrarGrupo.html'
    data = request.session.get('cookie_session', '')
    maestro = models.maestros.objects.get(usuario = data)
    grupo = models.grupo.objects.filter(idMaestro = maestro.id).exists()
    if request.method == 'GET':
        if data:
            if grupo == True:
                alumnos = models.alumnos.objects.filter(idMaestro = maestro.id).exists()
                if alumnos == True:
                    alumnos = models.alumnos.objects.filter(idMaestro = maestro.id)
                    grupo = models.grupo.objects.get(idMaestro = maestro.id)
                    return render(request, template, {'docente': data, 'grupo': 1, 'alumnos': alumnos, 'gpo': grupo})
                elif alumnos == False:
                    grupo = models.grupo.objects.get(idMaestro = maestro.id)
                    return render(request, template, {'docente': data, 'grupo': 1, 'gpo': grupo})
            elif grupo == False:
                return render(request, template, {'docente': data, 'grupo': 0})
        else:
            return redirect(redirectLogin)
    if request.method == 'POST':
        asignatura = request.POST.get('setAsig')
        turno = request.POST.get('turno')
        init_date = request.POST.get('dateInit')
        final_date = request.POST.get('dateInit')

        obj = models.grupo(
            idMaestro=maestro,
            asignatura=asignatura, 
            turno=turno,
            initDate=init_date,
            finalDate=final_date
        )
        obj.save()

        return render(request, template, {'docente': data, 'grupo': 1})

def mostrar_actividades(request):
    template = 'mostrarActividades.html'
    data = request.session.get('cookie_session', '')
    if request.method == 'GET':
        if data:
            #Se obtiene el objeto del alumno
            alumno = models.alumnos.objects.get(usuario = data)
            #Se verifica si el alumno ha sido agregado a un grupo
            grupo = models.grupo.objects.filter(idMaestro = alumno.idMaestro_id).exists()
            #Si el alumno ya fue agregado a un grupo
            if grupo == True:
                #Se comprueba si hay actividades
                actividades = models.ejercicios.objects.filter(idMaestro = alumno.idMaestro_id).exists()
                #Se obtiene el objeto de grupo en donde se encuentra el alumno
                asignado = models.grupo.objects.get(idMaestro_id = alumno.idMaestro_id)
                if actividades == True:
                    return render(request, template, {'grupo': 1, 'actividades': 1, 'valor': asignado, 'activs': actividades})
                elif actividades == False:
                    return render(request, template, {'grupo': 1, 'actividades': 0, 'valor': asignado})
            elif grupo == False:
                return render(request, template, {'grupo': 0})
        else:
            return redirect(redirectLogin)

def crear_actividades(request):
    template = 'crearActividades.html'
    data = request.session.get('cookie_session', '')
    maestro = models.maestros.objects.get(usuario = data)
    grupo = models.grupo.objects.filter(idMaestro = maestro.id).exists()
    if request.method == 'GET':
        if data:
            if grupo == True:
                #Si hay grupo se comprueba si hay alumnos en el grupo ya registrado
                hayalumnos = models.alumnos.objects.filter(idMaestro_id = maestro.id).exists()
                if hayalumnos == True:
                    #Si hay alumnos registrados, se regresa la página con la opcion de crear actividad
                    #Se obtiene el objeto de grupo en donde se encuentran los alumnos
                    grupo = models.grupo.objects.get(idMaestro_id = maestro.id)
                    return render(request, template, {'grupo': 1, 'alumnos': 1, 'actividad': 1, 'valor': grupo})
                elif hayalumnos == False:
                    #Se obtiene el objeto de grupo en donde se encuentra el alumno
                    grupo = models.grupo.objects.get(idMaestro_id = maestro.id)
                    return render(request, template, {'grupo': 1, 'alumnos': 0, 'valor': grupo})
            elif grupo == False:
                return render(request, template, {'grupo': 0})
        else:
            return redirect(redirectLogin)
    if request.method == 'POST':
        #Recuperar datos
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        sEntradas = request.FILES.get('entrada')
        sSalida = request.FILES.get('salida')
        sInicializacion = request.FILES.get('inicializacion')
        sEdoFinal = request.FILES.get('estado')
        sParametros = request.FILES.get('parametros')

        #Validar extensión de scripts - regresa 0 = todo ok, 1 = vacío, 2 = la extensión o algo no es válido
        entrada = validar_extension(sEntradas)
        salida = validar_extension(sSalida)
        inicializacion = validar_extension(sInicializacion)
        estado = validar_extension(sEdoFinal)
        parametros = validar_extension(sParametros)

        #Después de validar la extensión, si el archivo es válido, se lee y regresa el contenido en el caso de 
        #los scripts de entrada y salida, el proceso es diferente para los script de inicializacion, edo y param
        ventrada = regresar_es(entrada)
        vsalida = regresar_es(salida)

        #Ahora verificamos la correcta estructura del arreglo, los dos posibles resultados son:
        #1. archivo válido, nombre del archivo, texto sin saltos y por lineas [0, 'nombre.txt', 'texto\ncompleto']
        #2. archivo inválido o vacío y nombre del archivo [1 o 2, 'nombre.txt']
        if ventrada[0] == 0:
            arreglo_entrada = quitar_saltos_vacios(ventrada)
        else:
            arreglo_entrada = ventrada

        if vsalida[0] == 0:
            arreglo_salida = quitar_saltos_vacios(vsalida)
        else:
            arreglo_salida = vsalida

        #Guardamos los datos a modo de prueba si no pasan posteriores verificaciones se eliminarán
        # try:
        #     obj = models.ejercicios(
        #         idMaestro=maestro,
        #         titulo=titulo,
        #         descripcion=descripcion,
        #         sInicializacion=sInicializacion,
        #         sEntradas=sEntradas,
        #         sSalida=sSalida,
        #         sParametros=sParametros,
        #         sEdoFinal=sEdoFinal,
        #         visible=0
        #     )
        #     obj.save()
        # except Exception as e:
        #     print(e)
        
        #para el script de inicializacion si fue proporcionado lo ejecutaremos con las credenciales dadas, en el directorio root del
        #usuario default y retornaremos el resultado de la ejecución
        if inicializacion[0] == 0:
            arreglo_inicializacion = ejecutar_inicializacion_maestro(inicializacion, maestro, titulo)
        else:
            arreglo_inicializacion = {'estado': inicializacion[0]}
        
        if estado[0] == 0:
            arreglo_estado = leer_sparametros(estado)
        else:
            arreglo_estado = {'estado': estado[0]}

        if parametros[0] == 0:
            arreglo_parametros = leer_sparametros(parametros)
        else:
            arreglo_parametros = {'estado': parametros[0]}

        contexto = {
            'titulo': titulo,
            'desc': descripcion,
            'entrada': arreglo_entrada,
            'salida': arreglo_salida,
            'init': arreglo_inicializacion,
            'estado': arreglo_estado,
            'parametros': arreglo_parametros
            }
        return render(request, 'analizarParametros.html', contexto)

def validar_extension(archivo):
    if archivo is None:
        return [1, archivo]
    else:
        extension = archivo.name
        extension = extension.split('.')
        if extension[1] == 'txt' or extension[1] == 'py' or extension[1] == 'sh':
            return [0, archivo]
        else:
            return [2, archivo]

def quitar_saltos_vacios(arreglo):
    contenido = ''
    for line in arreglo[2]:
        if line == b'\r\n':
            pass
        else:
            contenido += line.decode('utf-8').strip() + '\n'

    return {'estado': 0,'nombre': arreglo[1],'contenido': contenido.strip()}

def regresar_es(arreglo):
    if arreglo[0] == 2:
        return [2, arreglo[1].name]
    elif arreglo[0] == 1:
        return [1, arreglo[1].name]
    elif arreglo[0] == 0:
        contenido = arreglo[1].readlines()
        return [0, arreglo[1].name, contenido]

def ejecutar_inicializacion_maestro(arreglo, maestro, titulo):
    if arreglo[0] == 2:
        return {'estado': 2,'nombre': arreglo[1].name}
    elif arreglo[0] == 1:
        return {'estado': 1,'nombre': arreglo[1].name}
    elif arreglo[0] == 0:
        scriptname = arreglo[1].name
        script = scriptname.split('.')
        if script[1] == 'txt':
            #Si el script de inicializacion es txt se regresa como no válido
            return {'estado': 2,'nombre': arreglo[1].name}
        else:
            #Si la extensión del script es válido se obtiene la ruta de donde esta guardado el archivo de inicializacion y la ruta del
            #usuario default que ejecutará el script
            obj = models.ejercicios.objects.get(titulo = titulo, idMaestro_id=maestro.id)
            rutarchivo = obj.sInicializacion
            rutacompletarchivo = BASE_DIR.joinpath('media/' + str(rutarchivo))
            rutaroot = BASE_DIR.joinpath('environment/')

            #Se crea un directorio de test para el maestro únicamente para la ejecución del analisis preliminar, una vez ejecutado
            #si los datos son correctos se elimina el directorio con su contenido
            title = re.sub(r"\s+", "", titulo) #eliminar espacios en el titulo para el nombre de carpeta
            if not os.path.exists(str(rutaroot) + '/' + title):
                os.makedirs(str(rutaroot) + '/' + title)
                default_home = str(rutaroot) + '/' + title
                default_home = default_home.strip()
                shutil.copy(rutacompletarchivo, default_home)

                #Teniendo el archivo, se ejecuta bajo el usuario default dependiendo de la extensión
                if script[1] == 'py':
                    #Inicializar variables vacias por si no se crea directorio o usuario mas adelante
                    tree = ''
                    usuario = ''
                    install = ''
                    extra = ''
                    ex = 0

                    #Se da permisos a la carpeta y a su contenido de escritura para la ejecución por el usuario default
                    os.chdir(str(rutaroot))
                    os.system(f'chmod -R 757 {title}')

                    comando = default_home + '/' + scriptname
                    command = f'python3 {comando}'
                    p = os.popen(f'su - default -c "{command}"').read()

                    #Leer archivo
                    archivo = open(comando, 'r')
                    contenido = archivo.read()
                    
                    #Si p es vacio significa que el comando no regreso ninguna salida estándar y la ejecución fue correcta
                    if p == '':
                        #verificar si el archivo tiene código
                        if contenido != '':
                            #Verificar si se creo directorio
                            try:
                                indice = contenido.index('makedirs')
                            except:
                                indice = ''
                            
                            if indice != '':
                                command = f'tree'
                                tree = os.popen(f'su - default -c "{command}"').read()
                                ex = 1

                            #Verificar si se creo usuario
                            try:
                                uindice = contenido.index('useradd')
                            except:
                                uindice = ''

                            if uindice != '':
                                command = 'tail -1 /etc/passwd'
                                time.sleep(0.5)
                                usuario = os.popen(f'su - default -c "{command}"').read()
                                ex = 1
                            
                            #Si no entró en los casos establecidos, regresa el contenido del archivo únicamente
                            if ex == 0:
                                extra = contenido
                        else:
                            return {'estado': 2,'nombre': arreglo[1].name}
                    elif contenido.index('pip'):
                        install = p 
                    else:
                        return {'estado': 2,'nombre': arreglo[1].name}
                elif script[1] == 'sh':
                    pass
                else:
                    return {'estado': 2,'nombre': arreglo[1].name}

                contenido = {
                    'dir': tree,
                    'user': usuario,
                    'pip': install,
                    'extra': extra
                }
                #Borramos la carpeta temporal del análisis preliminar
                if os.path.exists(str(rutaroot) + '/' + title):
                    emptyornot = os.listdir(str(rutaroot) + '/' + title)
                    if emptyornot == 0:
                        command = 'rmdir ' + str(rutaroot) + '/' + title
                        os.system(f'su - default -c "{command}"')
                    else:
                        command = 'rm -r ' + str(rutaroot) + '/' + title
                        os.system(f'su - default -c "{command}"')
                return {'estado': 0,'nombre': arreglo[1].name,'contenido': contenido}
            else:
                return {'estado': 2,'nombre': arreglo[1].name}

def leer_sparametros(arreglo):
    contenido = arreglo[1].read()
    plano = contenido.decode('utf-8')
    return {'estado': 0,'nombre': arreglo[1].name,'contenido': plano}


def analizar_parametros(request):
    template = 'analizarParametros.html'
    data = request.session.get('cookie_session', '')
    if request.method == 'GET':
        if data:
            return render(request, template)
    elif request.method == 'POST':
        if request.POST.get('yes'):
            print("SE PULSO SI")
        elif request.POST.get('no'):
            titulo = request.POST.get('htitle')
            obj = models.ejercicios.objects.get(titulo = titulo)
            lista = existe_archivo(obj)

            for archivo in lista:
                command = f'rm {archivo}'
                os.system(command)

            obj.delete()
            return redirect('/crear')

def existe_archivo(objeto):
    arr = []
    if objeto.sInicializacion != '':
        rutaini = objeto.sInicializacion
        rutaini = BASE_DIR.joinpath('media/' + str(rutaini))
        arr.append(rutaini)
    
    if objeto.sEntradas != '':
        rutae = objeto.sEntradas
        rutae = BASE_DIR.joinpath('media/' + str(rutae))
        arr.append(rutae)
    
    if objeto.sSalida != '':
        rutas = objeto.sSalida
        rutas = BASE_DIR.joinpath('media/' + str(rutas))
        arr.append(rutas)
    
    if objeto.sParametros != '':
        rutap = objeto.sParametros
        rutap = BASE_DIR.joinpath('media/' + str(rutap))
        arr.append(rutap)
    
    if objeto.sEdoFinal != '':
        rutaf = objeto.sEdoFinal
        rutaf = BASE_DIR.joinpath('media/' + str(rutaf))
        arr.append(rutaf)
    
    return arr

# UPLOAD FILES
def uploadFile(request):
    x = 'upload.html'
    if request.method == 'GET':
        return render(request, x, {})
    elif request.method == 'POST':
        if request.POST.get('subir'):
            # Fetching the form data
            fileTitle = request.POST.get("fileTitle")
            file = request.FILES.get("file")
            # print(file) #Regresa el nombre del archivo

            # Saving the information in the database
            document = models.testfiles(title = fileTitle, uploaded = file)
            document.save()

            return redirect('/registros')
        else:
            return redirect('/registros')

def registros(request):
    x = 'uploadregis.html'
    if request.method == 'GET':
        documents = models.testfiles.objects.all()
        return render(request, x, context = {"files": documents})