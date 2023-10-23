# app/__init__.py
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
#from config import Config
import os
import threading
import time

import datetime
from sqlalchemy import text
import schedule
from redNeuronal.preprocesamiento import preprocess_data
import tensorflow as tf
import pandas as pd
import numpy as np
import requests
from flask_socketio import SocketIO


# Función que se ejecutará constantemente en un hilo separado



# Genera una clave secreta aleatoria

# TELEFERICO: -16.537835, -68.087510
# FINALES DEL COLEGIO: -16.536264, -68.086835
# CENTRO DE LA EMI: -16.534927, -68.086476
# MEGACENTER: -16.533322, -68.086227



app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la sesión
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/tramos_yungas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

MODELO = os.path.join('redNeuronal')
app.config['UPLOAD_MODELO'] = MODELO
modelo_mlp = os.path.join(app.config['UPLOAD_MODELO'],'mlp_model.h5')
model = tf.keras.models.load_model(modelo_mlp)

# Manejar evento de conexión de Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado:', request.sid)


# ESTRUCTURA DE LOS PUNTOS DEFINIDOS

tramos = [[1,-16.537835, -68.087510],
            [2,-16.536264, -68.086835],
            [3,-16.534927, -68.086476],
            [4,-16.533322, -68.086227],
            [5,-16.400028278131167,-67.71950883630169],
            [6,-16.401757380663387,-67.64447135595758],
            [7,-16.37379355606211,-67.58384238148729],
            [8,-16.380675956463296,-67.53964877102905],
            [9,-16.396560648229226,-67.4787238654091],
            [10,-16.428441272715645,-67.4674779353273],
            [11,-16.473003,-67.453236]]
'''
tramos = [[1,-16.469049472495275,-68.11605575655983],
            [2,-16.350058724719574,-68.0403933224296],
            [3,-16.327407122887553,-67.95503898847265],
            [4,-16.323726669715715,-67.8260676361114],
            [5,-16.400028278131167,-67.71950883630169],
            [6,-16.401757380663387,-67.64447135595758],
            [7,-16.37379355606211,-67.58384238148729],
            [8,-16.380675956463296,-67.53964877102905],
            [9,-16.396560648229226,-67.4787238654091],
            [10,-16.428441272715645,-67.4674779353273],
            [11,-16.473003,-67.453236]]
'''
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

# ESTRUCTURA PARA GUARDAR LAS UBICACIONES EN TIEMPO REAL DE LOS USUARIOS

datos_envio = {}

datos_para_enviar = {'mostrar':False,
                     'ultima_hora':'00:00',
                     'ultima_ubicacion':'NO HAY',
                     'pasajeros':0,
                     'nombre_conductor':'NO HAY',
                     'tipo_alerta':0}


ubicacion_usuarios = {}

def actualizar_ubicacion(usuario_id,latit,longit):
    ubicacion_usuarios[usuario_id] = {'latitud': latit, 'longitud': longit}

def eliminar_usuario(usuario_id):
    if usuario_id in ubicacion_usuarios:
        del ubicacion_usuarios[usuario_id]


def monitoreo_tiempo():
    #while True:


    apiKey = '13c065e6f69c21927ac4f66b8f7ddf9e'
    ciudadId = "3911925"

    # URL de la API de OpenWeatherMap para obtener el clima actual por ciudad
    url = f'https://api.openweathermap.org/data/2.5/weather?id=${ciudadId}&appid=${apiKey}&units=metric'

    # Realizar la solicitud a la API
    response = requests.get(url)

    clima_actual = 1

    if response.status_code == 200:
        # Obtener los datos de la respuesta en formato JSON
        datos_clima = response.json()

        # Acceder a los datos que necesitas, por ejemplo, la temperatura
        descripcion_clima = datos_clima['weather'][0]['description']
        descripcionClima = str(descripcion_clima)
        if(descripcionClima=='clear sky'):
            descripcionClima = 'Soleado'
            clima_actual = 1
        elif (descripcionClima=='few clouds'): 
            descripcionClima = 'Soleado'
            clima_actual = 1
        elif (descripcionClima=='scattered clouds'):
            descripcionClima = 'Soleado'
            clima_actual = 1
        elif (descripcionClima=='broken clouds'):
            descripcionClima = 'Ventoso'
            clima_actual = 8
        elif (descripcionClima=='overcast clouds'):
            descripcionClima = 'Nublado'
            clima_actual = 2
        elif (descripcionClima=='mist'):
            descripcionClima = 'Niebla'
            clima_actual = 7
        elif (descripcionClima=='fog'):
            descripcionClima = 'Niebla'
            clima_actual = 7
        elif (descripcionClima=='light rain'):
            descripcionClima = 'Lluvioso'
            clima_actual = 3
        elif (descripcionClima=='moderate rain'):
            descripcionClima = 'Lluvioso'
            clima_actual = 3
        elif (descripcionClima=='heavy rain'):
            descripcionClima = 'Lluvioso'
            clima_actual = 3
        elif (descripcionClima=='light snow'):
            descripcionClima = 'Nieve'
            clima_actual = 5
        elif (descripcionClima=='moderate snow'):
            descripcionClima = 'Nieve'
            clima_actual = 5
        elif (descripcionClima=='heavy snow'):
            descripcionClima = 'Nieve'
            clima_actual = 5
        elif (descripcionClima=='thunderstorm'):
            descripcionClima = 'Tormenta electrica'
            clima_actual = 4
        elif (descripcionClima=='drizzle'):
            descripcionClima = 'Lluvioso'
            clima_actual = 3
        elif (descripcionClima=='freezing rain'):
            descripcionClima = 'Granizo'
            clima_actual = 6
        elif (descripcionClima=='sleet'):
            descripcionClima = 'Granizo'
            clima_actual = 6
        else:
            descripcionClima = 'Ventoso'
            clima_actual = 8
        

        # Hacer algo con la temperatura actual
        # print(f'Temperatura actual: {descripcion_clima}°C')



    print("Buscando autos atrasados")
    fecha_hora_actual = datetime.datetime.now()
    hora = fecha_hora_actual.hour
    minuto = fecha_hora_actual.minute
    hora = float(hora)
    minuto = float(minuto)
    minuto = minuto/60
    hora_actual = hora+minuto
    viajesActuales = ''
    # se hara prueba otro sql = text("SELECT * FROM viajes WHERE estado_viaje = :destino")
    sql = text("SELECT viajes.id_viaje, viajes.hora_inicio, viajes.hora_ultimo, viajes.id_tramo_viaje, viajes.ultima_ubicacion, viajes.id_auto_viaje, viajes.pasajeros, viajes.estado_emb, tramos.tiempo_ida, tramos.zona_riesgosa FROM viajes INNER JOIN tramos ON viajes.id_tramo_viaje = tramos.id_tramo WHERE viajes.estado_viaje= :destino")
        
        # Pasar el objeto text() a db.session.execute()
        #result = db.session.execute(sql, {"destino": "Paris"})
    with app.app_context():
        viajesActuales = db.session.execute(sql, {"destino": "En camino"})
    viajesActuales = list(viajesActuales)
    for viaje in viajesActuales:

        if(str(viaje.estado_emb)=='A tiempo'):

            print(viaje.id_viaje)

            print(viaje.hora_ultimo)
            hora_base = str(viaje.hora_ultimo)
            hora_base = hora_base[-8:]
            hora_base = hora_base[:5]
            print(hora_base)
            horas = float(hora_base[:2])
            minutos = float(hora_base[-2:])
            minutos = minutos/60
            tiempo_tramo = int(viaje.tiempo_ida)
            tiempo_total = tiempo_tramo+15

            # hora_base2 = hora_base[:2]+hora_base[-2:]
            hora_base2 = horas + minutos

            print(hora_base)
            hora_base2 = float(hora_base2)
            id_viajesi = int(viaje.id_viaje)
            diferencia = hora_actual-hora_base2
            diferencia = int(diferencia*60)




            if(diferencia>=tiempo_total):

                print('ACTIVAR IA')

                id_auto_viaje = int(viaje.id_auto_viaje)
                pasajeros = int(viaje.pasajeros)
                ultima_ubicacion = str(viaje.ultima_ubicacion)


                sql2 = text("SELECT usuarios.id_usuario, usuarios.ci_usuario, persona.nombre, autos.id_auto FROM usuarios INNER JOIN persona ON usuarios.ci_usuario=persona.ci INNER JOIN autos ON autos.id_chofer=usuarios.id_usuario WHERE autos.id_auto= :id_conductor")
        
                    # Pasar el objeto text() a db.session.execute()
                    #result = db.session.execute(sql, {"destino": "Paris"})
                with app.app_context():
                    datos_conductor = db.session.execute(sql2, {"id_conductor": id_auto_viaje})
                datos_conductor = list(datos_conductor)

                nombre_conductor = datos_conductor[0].nombre

                hora_inicio = str(viaje.hora_inicio)
                hora_inicio = hora_inicio[-8:]
                hora_inicio = hora_inicio[:5]
                fecha_actual = str(viaje.hora_ultimo)
                fecha_actual = fecha_actual[:10]
                fecha_actual = fecha_actual[-5:]
                dias = fecha_actual[-2:]
                mes = fecha_actual[2:]
                dias = float(dias)
                dias = (dias-1)/31
                mes = float(mes)
                mes = mes-1
                fecha_actual=float(mes+dias)
                dias_pasados = (fecha_actual*365)/12
                estacion_actual = 1
                dias_pasados = int(dias_pasados)
                if(dias_pasados>=264 and dias_pasados<353):
                    print("primavera")
                    estacion_actual=3
                elif(dias_pasados>=173 and dias_pasados<264):
                    print("invierno")
                    estacion_actual=1
                elif(dias_pasados>=82 and dias_pasados<173):
                    print("otoño")
                    estacion_actual=2
                else:
                    print("verano")
                    estacion_actual=4

                #hora_base
                ult_punto = int(viaje.id_tramo_viaje)
                clima = clima_actual
                estacion = estacion_actual
                riesgo = int(viaje.zona_riesgosa)
                t_tramo = tiempo_tramo

                prediction = None

                #data = np.array([hora_inicio,hora_base,ult_punto,clima,estacion,riesgo,t_tramo])
                data = {"h_inicio":hora_inicio,
                        "h_ultimo":hora_base,
                        "u_ubicacion":ult_punto,
                        "clima":clima,
                        "estacion":estacion,
                        "riesgo":riesgo,
                        "t_tramo":t_tramo}

                df = preprocess_data(pd.DataFrame([data]))
                prediction = model.predict(df.values.reshape(1, df.shape[1], 1))
                prediction = "Alerta" if prediction > 0.5 else "Sin alerta"

                if(prediction=="Alerta"):

                    datos_envio = {'ultima_hora': hora_base,'ultima_ubicacion':ultima_ubicacion,'nombre':nombre_conductor,'pasajeros':pasajeros,'embarrancamiento':1}
                    nuevos_datos_para_enviar = {'mostrar':True,
                     'ultima_hora':hora_base,
                     'ultima_ubicacion':ultima_ubicacion,
                     'pasajeros':pasajeros,
                     'nombre_conductor':nombre_conductor,
                     'tipo_alerta':1}
                    '''datos_para_enviar['mostrar']=True
                    datos_para_enviar['ultima_hora']=hora_base
                    datos_para_enviar['ultima_ubicacion']=ultima_ubicacion
                    datos_para_enviar['nombre_conductor']=nombre_conductor
                    datos_para_enviar['pasajeros']=pasajeros
                    datos_para_enviar['tipo_alerta']=1'''
                    datos_para_enviar.update(nuevos_datos_para_enviar)
                    for dat,valor in datos_para_enviar.items():
                        print(dat,":",valor)
                    #socketio.emit('envio_datos',nuevos_datos_para_enviar)
                    #enviar_alerta(hora_base, ultima_ubicacion, nombre_conductor, pasajeros,1)
                    #enviar_alerta()
                    enviar_datos()
                    print("es alerta de embarrancamiento")
                    with app.app_context():
                        sql1 = text("UPDATE viajes SET estado_emb = :estadoemb WHERE id_viaje = :id_via")
                        db.session.execute(sql1, {"estadoemb": "Embarrancamiento","id_via":id_viajesi})
                        db.session.commit()
                else:
                    datos_envio = {'ultima_hora': hora_base,'ultima_ubicacion':ultima_ubicacion,'nombre':nombre_conductor,'pasajeros':pasajeros,'embarrancamiento':0}
                    nuevos_datos_para_enviar = {'mostrar':True,
                     'ultima_hora':hora_base,
                     'ultima_ubicacion':ultima_ubicacion,
                     'pasajeros':pasajeros,
                     'nombre_conductor':nombre_conductor,
                     'tipo_alerta':2}
                    datos_para_enviar.update(nuevos_datos_para_enviar)
                    enviar_datos()
                    #socketio.emit('envio_datos',nuevos_datos_para_enviar)
                    '''datos_para_enviar['mostrar']=True
                    datos_para_enviar['ultima_hora']=hora_base
                    datos_para_enviar['ultima_ubicacion']=ultima_ubicacion
                    datos_para_enviar['nombre_conductor']=nombre_conductor
                    datos_para_enviar['pasajeros']=pasajeros
                    datos_para_enviar['tipo_alerta']=2'''
                    for dat,valor in datos_para_enviar.items():
                        print(dat,":",valor)
                    
                    #enviar_alerta(hora_base, ultima_ubicacion, nombre_conductor, pasajeros,0)
                    #enviar_alerta()
                    print("probablemente no ocurrio nada")
                    with app.app_context():
                        sql1 = text("UPDATE viajes SET estado_emb = :estadoemb WHERE id_viaje = :id_via")
                        db.session.execute(sql1, {"estadoemb": "Posible Alerta","id_via":id_viajesi})
                        db.session.commit()


            else:
                print('No activar aun')
                '''
                with app.app_context():
                    sql1 = text("UPDATE viajes SET estado_emb = :estadoemb WHERE id_viaje = :id_via")
                    db.session.execute(sql1, {"estadoemb": "A tiempo","id_via":id_viajesi})
                    db.session.commit()
                '''
        else:
            print("No se activa la IA, porque ya se activo anteriormente")
        
        #time.sleep(300)  # Espera 300 segundos o 5 minutos antes de la siguiente iteración


# Crea un hilo para ejecutar la función tarea_continua
#hilo = threading.Thread(target=monitoreo_tiempo)

# Inicia el hilo
#hilo.start()

def ejecutar_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Configurar la tarea programada para que se ejecute cada 5 minutos
schedule.every(1).minutes.do(monitoreo_tiempo)

# Iniciar la ejecución de schedule en un hilo aparte
schedule_thread = threading.Thread(target=ejecutar_schedule)
schedule_thread.start()


@app.route('/actualizar_ubicacion', methods=['POST'])
def actualizar_ubicacion():
    data = request.json  # Obtener los datos enviados desde el cliente (latitud y longitud)
    
    # Procesar los datos como sea necesario (por ejemplo, imprimirlos en la terminal)
    print(f'Latitud: {data["latitude"]}, Longitud: {data["longitude"]}')
    
    # Puedes enviar una respuesta de vuelta al cliente si es necesario
    return jsonify({"message": "Ubicación actualizada correctamente"})

# from app import routes, models // chat gpt


# Lógica para enviar ubicaciones a través de Socket.IO en intervalos regulares (simulado)
def enviar_ubicaciones():
    while True:
        socketio.emit('ubicaciones_actualizadas', ubicacion_usuarios)
        socketio.sleep(5)  # Enviar cada 5 segundos (puedes ajustar el intervalo según tus necesidades)

def enviar_datos():
    #while True:
    print("Impresion de que se esta enviando socket")
    for dat,valor in datos_para_enviar.items():
        print(dat,":",valor)
    print("Se envio socket")

    socketio.emit('envio_datos', datos_para_enviar)
    socketio.sleep(20)

@socketio.on('datos_recibidos')
def manejar_mensaje(mensajito):
    print('Mensaje recibido desde el cliente:', mensajito)
    if(mensajito=="Llegaron los datos"):
        print("los datos llegaron al cliente apagar socket")
        nuevos_datos_para_enviar = {'mostrar':False,
                     'ultima_hora':'00:00',
                     'ultima_ubicacion':'NO HAY',
                     'pasajeros':0,
                     'nombre_conductor':'NO HAY',
                     'tipo_alerta':0}
        datos_para_enviar.update(nuevos_datos_para_enviar)
        print(datos_para_enviar['mostrar'])
    else:
        print("seguramente no habia nada para mostrar de los datos")
    # Puedes realizar acciones adicionales aquí según el mensaje recibido desde el cliente

def enviar_alerta():
    print("socket entro aqui")
    # Enviar notificación a todos los usuarios
    def on_notificacion_enviada():
        print("Notificación enviada al cliente.")
    print("Socket a punto de emitir un emit")
    socketio.emit('notificacion', datos_envio, callback=on_notificacion_enviada, include_self=True)
    print("Socket emitio el emit")
    return "Notificación enviada."
    

'''
def enviar_alerta(ultima_hora, ultima_ubicacion, nombre, pasajeros, tipo):
    ultima_hora_r=str(ultima_hora)
    ultima_ubicacion_r=str(ultima_ubicacion)
    nombre_conductor=str(nombre)
    pasajeros_r = str(pasajeros)
    tipo_emb = int(tipo)
    datos_envio = {'ultima_hora': ultima_hora_r,'ultima_ubicacion':ultima_ubicacion_r,'nombre':nombre_conductor,'pasajeros':pasajeros_r,'embarrancamiento':tipo_emb}
    print("socket entro aqui")

    # Enviar notificación a todos los usuarios
    def on_notificacion_enviada():
        print("Notificación enviada al cliente.")
    socketio.emit('notificaciones', datos_envio, callback=on_notificacion_enviada)
    return "Notificación enviada."
    
    #socketio.emit('notificaciones', {'ultima_hora': ultima_hora_r, 'ultima_ubicacion': ultima_ubicacion_r, 'nombre': nombre_conductor, 'pasajeros': pasajeros_r, 'embarrancamiento': tipo_emb})
'''


@app.route('/guardar_ubicacion/<id>/<id_tramo>/<destino>/<id_usuarios>', methods=['POST'])
def guardar_ubicacion(id,id_tramo,destino,id_usuarios):
    id_usuario = int(id_usuarios)
    data = request.get_json()
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    origen = data.get('origen')
    nombre_conductor = data.get('nombre_conductor')


    def actualizar_ubicacion1(usuario_id,latit,longit,orig,dest,nombre_co):
        ubicacion_usuarios[usuario_id] = {'latitud': latit, 'longitud': longit, 'origen': orig, 'destino':dest, 'nombre_c':nombre_co}

    def eliminar_usuario1(usuario_id):
        if usuario_id in ubicacion_usuarios:
            del ubicacion_usuarios[usuario_id]
    

    ubicacion = str(latitud)+';'+str(longitud)

    latitud = float(latitud)
    longitud = float(longitud)
    

    if(int(latitud)==0 and int(longitud)==0):
        eliminar_usuario1(id_usuario)
    else:
        print(id_usuario)
        print(latitud)
        print(longitud)

        actualizar_ubicacion1(id_usuario, latitud, longitud,origen,destino,nombre_conductor)
        for usuario_id,ubi in ubicacion_usuarios.items():
            print(usuario_id)
            print(ubi['latitud'])
            print(ubi['longitud'])

        # para determinar el tramo se esta tomando el valor de 500 m a la redonda
        # referencia 0.003584

        flag_actualizar_tramo = False
        id_tramo_actual = int(id_tramo)
        indice_tramo = 0
        operador=0
        if(str(destino)=="Irupana"):
            operador = 0
        else:
            operador = -1

        for tram in tramos:
            '''
            alto = float(tram[1])+0.003584
            bajo = float(tram[1])-0.003584
            izq = float(tram[2])-0.003584
            der = float(tram[2])+0.003584
            '''
            alto = float(tram[1])+0.000235
            bajo = float(tram[1])-0.000235
            izq = float(tram[2])-0.000235
            der = float(tram[2])+0.000235
            if((latitud>bajo and latitud<alto) and (longitud>izq and longitud<der)):
                indice_tramo = int(tram[0])
                if(indice_tramo!=1 and indice_tramo!=11):
                    flag_actualizar_tramo = True
                break

        if(flag_actualizar_tramo):
            id_tramo_actual = indice_tramo+operador
            id_tramo_actual = int(id_tramo_actual)
            if(id_tramo_actual==int(id_tramo)):
                flag_actualizar_tramo = False

            

        fecha_hora_actual = datetime.datetime.now()
        fecha_hora_actual = str(fecha_hora_actual)
        fecha_hora_actual =fecha_hora_actual[:19]
        print(fecha_hora_actual)

        

        if(flag_actualizar_tramo):
            sql_act_tramo = text("UPDATE viajes SET id_tramo_viaje = :id_t_viaj WHERE id_viaje = :id_viaj")
            with app.app_context():
                db.session.execute(sql_act_tramo, {"id_t_viaj":id_tramo_actual,"id_viaj": id})
                db.session.commit()

        sql_act = text("UPDATE viajes SET hora_ultimo = :h_ult WHERE id_viaje = :id_viaj")
        with app.app_context():
            db.session.execute(sql_act, {"h_ult":fecha_hora_actual,"id_viaj": id})
            db.session.commit()

        sql_act2 = text("UPDATE viajes SET ultima_ubicacion = :ult WHERE id_viaje = :id_viaj")
        with app.app_context():
            db.session.execute(sql_act2, {"ult": ubicacion,"id_viaj": id})
            db.session.commit()
        
        # Aquí puedes guardar la latitud y longitud en tu base de datos o hacer lo que desees
        # ...

        return jsonify({"mensaje": "Ubicación guardada correctamente"}), 200

from routes.login import login
from routes.admin import admin
from routes.usuario import usuario

app.register_blueprint(login)
app.register_blueprint(admin)
app.register_blueprint(usuario)








'''
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
'''