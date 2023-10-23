from flask import Flask,Blueprint, render_template, request, redirect
from app import db
import os
from models.viaje import Viajes
from models.sindicato import Autos
from models.usuario import Persona, Usuarios
from models.municipio import Tramos
from redNeuronal.preprocesamiento import preprocess_data
import pandas as pd
import tensorflow as tf
import datetime


from routes.autenticador import login_required






app = Flask(__name__)
IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
coche_logo_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_1.png')
coche_logo_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_2.png')
coche_logo_3 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_3.png')
coche_logo_4 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_4.png')
coche_logo_5 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_5.png')
coche_logo_6 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_6.png')
caseta_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'caseta.png')


MODELO = os.path.join('redNeuronal')
app.config['UPLOAD_MODELO'] = MODELO
modelo_mlp = os.path.join(app.config['UPLOAD_MODELO'],'mlp_model.h5')
model = tf.keras.models.load_model(modelo_mlp)


admin = Blueprint('admin', __name__)

@admin.route("/viajes")
@login_required
def inicioAdmin():
    viajesActuales = Viajes.query.where(Viajes.estado_viaje!='Completado')
    mostrarMap = False

    if not viajesActuales:
        mostrarMap = False
    else:
        mostrarMap = True
    viajesActuales = list(viajesActuales)
    numero=0

    

    for viaj in viajesActuales:
        hora_inicio = str(viaj.hora_inicio)
        hora_inicio = hora_inicio[-8:]
        #print(hora_inicio)
        viaj.hora_inicio=hora_inicio
        usuarioAuto = Autos.query.where(Autos.id_auto==viaj.id_auto_viaje)
        #print(usuarioAuto[0])
        usuarioAuto = int(usuarioAuto[0].id_chofer)
        #print(usuarioAuto)
        personaAuto = Usuarios.query.where(Usuarios.id_usuario==usuarioAuto)
        #print(personaAuto[0])
        personaAuto = int(personaAuto[0].ci_usuario)
        #print(personaAuto)
        nombreConductor = Persona.query.where(Persona.ci==personaAuto)
        #print(nombreConductor[0])
        nombreConductor = str(nombreConductor[0].nombre)
        #print(nombreConductor)
        viaj.nconductor = nombreConductor
        viaj.cont = numero+1
        #print(viaj.cont)
        numero=numero+1
        opciones = list([True,False,False])
        viaj.atiempo = False
        viaj.embarrancado = False
        viaj.otrofallo = False
        ubicacion = str(viaj.ultima_ubicacion)

        puntos_pasados = [False,False,False,False,False,False,False,False,False,False,False]

        if(str(viaj.origen)=='La Paz'):
            indice_limite = int(viaj.id_tramo_viaje)  # Cambiar hasta el índice 5 (0 a 5 inclusivo)
            for indice, valor in enumerate(puntos_pasados):
                if indice < indice_limite:
                    puntos_pasados[indice] = True
            
        else:
            indice_limite = int(viaj.id_tramo_viaje)-1  # Cambiar hasta el índice 5 (0 a 5 inclusivo)
            for indice, valor in enumerate(puntos_pasados):
                if indice > indice_limite:
                    puntos_pasados[indice] = True

        print("un viaje: ",int(viaj.id_tramo_viaje))

        for i in puntos_pasados:
            print(i)


        viaj.tramos_pasados=puntos_pasados

        if(ubicacion=="La Paz"):
            viaj.latitud = -16.468436
            viaj.longitud = -68.115620
        elif(ubicacion=="Irupana"):
            viaj.latitud = -16.471911
            viaj.longitud = -67.452503
        else:
            lati = ubicacion.split(";")[0]
            longi = ubicacion.split(";")[1]
            
            viaj.latitud = lati
            viaj.longitud = longi
        
        if(viaj.estado_emb=='A tiempo'):
            viaj.atiempo = True
        elif(viaj.estado_emb=='Embarrancamiento'):
            viaj.embarrancado= True
        else:
            viaj.otrofallo = True


    return render_template('listActuales.html', user_image=Flask_Logo, viajesAct=viajesActuales, nums = numero, mostrarMapa = mostrarMap)



@admin.route("/completados")
@login_required
def viajesTerminados():
    viajesCompletados = Viajes.query.where(Viajes.estado_viaje=='Completado')
    viajesCompletados = list(viajesCompletados)
    numero=0

    for viaj in viajesCompletados:
        
        usuarioAuto = Autos.query.where(Autos.id_auto==viaj.id_auto_viaje)
        print(usuarioAuto[0])
        usuarioAuto = int(usuarioAuto[0].id_chofer)
        print(usuarioAuto)
        personaAuto = Usuarios.query.where(Usuarios.id_usuario==usuarioAuto)
        personaAuto = int(personaAuto[0].ci_usuario)
        print(personaAuto)
        nombreConductor = Persona.query.where(Persona.ci==personaAuto)
        nombreConductor = str(nombreConductor[0].nombre)
        print(nombreConductor)
        #viaj.id_auto_viaje = nombreConductor
        viaj.nconductor = nombreConductor
        print(viaj.id_auto_viaje)
        viaj.cont = numero+1
        print(viaj.cont)
        numero=numero+1


    return render_template('listCompletados.html', user_image=Flask_Logo, viajesAct=viajesCompletados)


@admin.route("/usuarios")
@login_required
def listaUsuarios():
    listUsers = Usuarios.query.where(Usuarios.rol_usuario!=1)
    listUsers = list(listUsers)
    numero=0

    for user in listUsers:

        user.nrol=''

        if(user.rol_usuario==2):
            user.nrol='Administrador'
        else:
            user.nrol='Usuario'

        ci_us = int(user.ci_usuario)

        datosPersona = Persona.query.where(Persona.ci==ci_us)
        nombre = str(datosPersona[0].nombre)
        cargo = str(datosPersona[0].rol_sindicato)
        telefono = int(datosPersona[0].telefono)
        user.name = nombre
        user.cargo = cargo
        user.telefono = telefono
        user.chofer = False
        if(user.cargo=='Conductor'):
            datosAuto = Autos.query.where(Autos.id_chofer==user.id_usuario)
            user.id_auto = int(datosAuto[0].id_auto)
            user.placa = str(datosAuto[0].placa)
            user.marca = str(datosAuto[0].marca)
            user.color = str(datosAuto[0].color)
            user.chofer = True
        
        user.cont = numero+1
        
        numero=numero+1


    return render_template('listUsuarios.html', user_image=Flask_Logo, users=listUsers)


@admin.route("/nuevoViaje")
@login_required
def nuevoViaje():
    autosExistentes = Autos.query.all()
    autosExistentes = list(autosExistentes)
    fecha_actual = datetime.datetime.now()
    fecha_actual = str(fecha_actual)
    fecha_actual = fecha_actual[:10]

    for aut in autosExistentes:
        users = Usuarios.query.where(Usuarios.id_usuario==aut.id_chofer)
        users = int(users[0].ci_usuario)
        nombrePersona = Persona.query.where(Persona.ci==users)
        nombrePersona = str(nombrePersona[0].nombre)
        aut.conductor = nombrePersona

    return render_template('agregarViaje.html', user_image=Flask_Logo, datosAut=autosExistentes, fecha=fecha_actual)


@admin.route("/crearViaje", methods=['POST'])
@login_required
def crearViaje():

    origen = request.form['origen']
    destino = ''
    fechaViaje = request.form['fechaViaje']
    horaPartida = request.form['horaPartida']
    horaFinal = ''
    estado = 'En Espera'
    ultimaUbicacion = origen
    cantidadPasajeros = int(request.form['cantidadPasajeros'])
    idAuto = int(request.form['idAuto'])
    idTramo = 1
    idAlerta = 1
    estado_emb = 'A tiempo'
    fecha_hora_actual = datetime.datetime.now()
    fecha_hora_actual = str(fecha_hora_actual)
    fecha_hora_actual =fecha_hora_actual[:19]

    if(origen=='La Paz'):
        destino='Irupana'
    else:
        destino='La Paz'
        idTramo = 10
    
    formatoF = str(fechaViaje)
    anno = formatoF[-4:]
    mes = formatoF[3:5]
    dia = formatoF[:2]
    #fechaViaje=anno+'-'+mes+'-'+dia
    
    horaPartida = str(fechaViaje)+' '+str(horaPartida)+':00'

    print(fechaViaje)
    print(horaPartida)
    print(idAuto)
    print(request.form['idAuto'])


    new_Viaje = Viajes(origen, destino, fechaViaje, horaPartida, horaFinal, estado, ultimaUbicacion, fecha_hora_actual, idAuto, cantidadPasajeros, idTramo, idAlerta, estado_emb)
    db.session.add(new_Viaje)
    db.session.commit()

    return redirect('/viajes')

@admin.route("/nuevoUsuario")
@login_required
def nuevoUsuario():

    return render_template('agregarUsuario.html', user_image=Flask_Logo)



@admin.route("/crearUsuario", methods=['POST'])
@login_required
def crearUsuario():

    nombre = request.form['nombreUsuario']
    ci = request.form['nci']
    telefono = request.form['telefono']
    cargo = request.form['cargo']
    nombreUs = request.form['nomUsuario']
    contrasena = request.form['contrasena']
    rol=2

    if(cargo=='Conductor'):
        rol=3

    sindicato = 1

    new_Persona = Persona(ci,nombre,telefono,cargo,sindicato)
    db.session.add(new_Persona)
    db.session.commit()

    new_Usuario = Usuarios(nombreUs,contrasena,rol,ci)
    db.session.add(new_Usuario)
    db.session.commit()

    if(rol==3):
        return render_template('/agregarAuto.html', ci_us=ci)

    return redirect('/usuarios')


@admin.route("/crearAuto", methods=['POST'])
@login_required
def crearAuto():

    placa = request.form['placa']
    ci = int(request.form['ciConductor'])
    print(ci)
    tCambio = request.form['tCambio']
    marca = request.form['marca']
    color = request.form['color']

    idUsuario = Usuarios.query.where(Usuarios.ci_usuario==ci)
    idUsuario = int(idUsuario[0].id_usuario)

    new_Auto = Autos(placa, tCambio, marca, color, idUsuario)
    db.session.add(new_Auto)
    db.session.commit()

    return redirect('/usuarios')



@admin.route("/modificarUsuario/<id>", methods=['POST', 'GET'])
@login_required
def modificarUsuario(id):

    if request.method == 'POST':
        nombre = request.form['nombreUsuario']
        telefono = request.form['telefono']
        cargo = request.form['cargoUsuario']
        nombreUs = request.form['nomUsuario']
        contrasena = request.form['contrasena']
        user = Usuarios.query.get(id)
        ci = user.ci_usuario
        person = Persona.query.get(ci)

        person.nombre = nombre
        person.telefono = telefono
        person.rol_sindicato = cargo

        user.nombre_usuario = nombreUs
        user.contrasena = contrasena

        db.session.commit()


    return redirect('/usuarios')



@admin.route('/predmanual', methods=['GET', 'POST'])
def prmanual():
    prediction = None
    if request.method == 'POST':
        # Aquí capturas los datos del formulario y los procesas
        data = dict(request.form)
        print(data)
        df = preprocess_data(pd.DataFrame([data]))
        prediction = model.predict(df.values.reshape(1, df.shape[1], 1))
        prediction = "Alerta" if prediction > 0.5 else "Sin alerta"

    return render_template('redManual.html', prediction=prediction, user_image=Flask_Logo,)


@admin.route("/verUbicaciones")
@login_required
def verUbicaciones():

    tramos_latitudes = [-16.469049472495275,
                    -16.350058724719574,
                    -16.327407122887553,
                    -16.323726669715715,
                    -16.400028278131167,
                    -16.401757380663387,
                    -16.37379355606211,
                    -16.380675956463296,
                    -16.396560648229226,
                    -16.428441272715645,
                    -16.473003]

    tramos_longitudes = [-68.11605575655983,
                        -68.0403933224296,
                        -67.95503898847265,
                        -67.8260676361114,
                        -67.71950883630169,
                        -67.64447135595758,
                        -67.58384238148729,
                        -67.53964877102905,
                        -67.4787238654091,
                        -67.4674779353273,
                        -67.453236]
    
    direcciones_coches = [coche_logo_1,coche_logo_2,coche_logo_3,coche_logo_4,coche_logo_5,coche_logo_6]


    return render_template('ubicacionesUsuarios.html', user_image=Flask_Logo, latitudes=tramos_latitudes,longitudes=tramos_longitudes,logo_coches=direcciones_coches, logo_caseta=caseta_logo)