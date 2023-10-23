# run.py
from app import app,db,socketio,enviar_ubicaciones,enviar_alerta,enviar_datos


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.start_background_task(enviar_alerta)  # Iniciar la tarea en segundo plano
    socketio.start_background_task(enviar_ubicaciones)  # Iniciar la tarea en segundo plan
    #socketio.start_background_task(enviar_datos)  # Iniciar la tarea en segundo plano
    
    print("Eventos de sockets registrados: ", socketio.server.handlers)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

'''
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
'''