from flask import Blueprint, redirect, request, Flask, render_template, session

from app import db
import os
from models.viaje import Viajes
from models.sindicato import Autos
from models.usuario import Persona, Usuarios

import datetime

from routes.autenticador import login_required


app = Flask(__name__)
IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
coche_logo_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'coche_1.png')

usuario = Blueprint('usuario', __name__)


@usuario.route("/espera")
@login_required
def inicioUsuario():

    id_usuario = session['user_id']
    estado_viaje = session['estado_viaje']
    id_auto_viajes = session['id_auto']

    if(estado_viaje):
        print("MOSTRAR UBICACION Y MANDAR UBICACION")
        queryViaje = Viajes.query.filter(Viajes.estado_viaje=='En camino',Viajes.id_auto_viaje==id_auto_viajes).all()
        dato_usuario = Usuarios.query.get(id_usuario)
        ci_usuario = int(dato_usuario.ci_usuario)
        dato_persona = Persona.query.get(ci_usuario)
        nombre_conductor = str(dato_persona.nombre)
        #datosViaje = list(queryViaje[0])
        id_viaje = queryViaje[0].id_viaje
        origen = queryViaje[0].origen
        destino = queryViaje[0].destino
        estado_v = queryViaje[0].estado_emb
        id_tramo = queryViaje[0].id_tramo_viaje
        return render_template('ubicacionReal.html', user_image = Flask_Logo, id_usuario = id_usuario, id_viaje = id_viaje, origen = origen, destino = destino, estado_viaje = estado_v, logo_auto = coche_logo_1, id_tramo_viaje = id_tramo, nombre_c = nombre_conductor)
    else:
        print("MOSTRAR LA TABLA DE VIAJES PROXIMOS")
        queryViaje = Viajes.query.filter(Viajes.estado_viaje=='En Espera',Viajes.id_auto_viaje==id_auto_viajes).all()
        datosViaje = list(queryViaje)

        if not queryViaje:
            vacios = False
        else:
            vacios = True
            for viaj in datosViaje:
                hora_ini = str(viaj.hora_inicio)
                hora_ini = hora_ini[-8:]
                viaj.hora_ini = hora_ini
        
        return render_template('tablaViajes.html', user_image=Flask_Logo, id_usuario = id_usuario, datos_viaje=datosViaje, vacios = vacios)

    #return render_template('inicioUsuario.html', user_image=Flask_Logo, id_usuario=id_usuario)


@usuario.route("/inicioViaje/<id>", methods=['POST', 'GET'])
@login_required
def iniciarViaje(id):

    if request.method == 'POST':
        pasajeros = request.form['cantidad_pasajeros']
        usuario = session['user_id']
        id_auto = session['id_auto']
        viaje = Viajes.query.get(id)
        
        fecha_hora_actual = datetime.datetime.now()
        fecha_hora_actual = str(fecha_hora_actual)
        fecha_hora_actual =fecha_hora_actual[:19]

        estado_viaje = "En camino"
        
        viaje.pasajeros = pasajeros
        viaje.hora_inicio = fecha_hora_actual
        viaje.hora_ultimo = fecha_hora_actual
        viaje.estado_viaje = estado_viaje

        session['estado_viaje']=True

        db.session.commit()


    return redirect('/espera')


@usuario.route("/finViaje/<id>")
@login_required
def finViaje(id):

    usuario = session['user_id']
    id_auto = session['id_auto']
    fecha_hora_actual = datetime.datetime.now()
    fecha_hora_actual = str(fecha_hora_actual)
    fecha_hora_actual =fecha_hora_actual[:19]
    viaje = Viajes.query.get(id)
    estado_viaje = "Completado"
    viaje.estado_viaje = estado_viaje
    viaje.hora_ultimo = fecha_hora_actual
    viaje.hora_final = fecha_hora_actual
    session['estado_viaje']=False

    db.session.commit()


    return redirect('/espera')




@usuario.route("/pasados")
@login_required
def viajesPasados():

    id_usuario = session['user_id']
    estado_viaje = session['estado_viaje']
    id_auto_viajes = session['id_auto']
    queryViaje = Viajes.query.filter(Viajes.estado_viaje=='Completado',Viajes.id_auto_viaje==id_auto_viajes).all()
    
    datosViaje = list(queryViaje)
    numero = 0

    for viaj in datosViaje:
        hora_ini = str(viaj.hora_inicio)
        hora_ini = hora_ini[-8:]
        viaj.hora_ini = hora_ini
        hora_fini = str(viaj.hora_final)
        hora_fini = hora_fini[-8:]
        viaj.hora_fini = hora_fini
        viaj.cont = numero+1
        numero = numero+1
        
    return render_template('usuarioCompletados.html', user_image=Flask_Logo, datos_viaje=datosViaje)

    #return render_template('inicioUsuario.html', user_image=Flask_Logo, id_usuario=id_usuario)