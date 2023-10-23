from flask import Flask,Blueprint, render_template, request, redirect, session
from models.usuario import Usuarios
from models.sindicato import Autos
from models.viaje import Viajes
from app import db
import os

app = Flask(__name__)

login = Blueprint('login', __name__)

IMG_FOLDER = os.path.join('static', 'IMG')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@login.route("/")
def inicioSesion():
    Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('index.html', user_image=Flask_Logo)

@login.route("/iniciarSesion", methods=['POST'])
def validarSesion():
    #print(request.form['usuario'])
    #print(request.form['contrasena'])
    usuarioIn = request.form['usuario']
    contrasenaIn = request.form['contrasena']
    datosDB = Usuarios.query.where(Usuarios.nombre_usuario==usuarioIn)
    if(datosDB.count()>=1):
        #print('existe usuario')
        #print(datosDB[0].contrasena)
        #print(datosDB[0].nombre_usuario)
        if(datosDB[0].contrasena==contrasenaIn):
            #print('Puede ingresar')
            rolUsuario = datosDB[0].rol_usuario
            session['logged_in']=True
            session['user_id']=datosDB[0].id_usuario
            if(rolUsuario==1 or rolUsuario==2):
                return redirect('/viajes')
            else:
                datosAuto = Autos.query.where(Autos.id_chofer==datosDB[0].id_usuario)
                idAuto = int(datosAuto[0].id_auto)
                datosViaje = Viajes.query.filter(Viajes.id_auto_viaje==idAuto, Viajes.estado_viaje=="En camino").all()
                session['id_auto']=idAuto

                if not datosViaje:
                    #print("No hay viajes en camino")
                    session['estado_viaje']=False
                else:
                    #print("Esta en camino de un viaje")
                    session['estado_viaje']=True

                return redirect('/espera')
        else:
            #print('contrasena incorrecta')
            return redirect('/')
    else:
        #print('no existe usuario')
        return redirect('/')
    return 'iniciando sesion'


@login.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/')