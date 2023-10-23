from app import db

class Nivel_alerta(db.Model):
    id_alerta = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))

    def __init__(self, descripcion):
        self.descripcion = descripcion


class Viajes(db.Model):
    id_viaje = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(50))
    destino = db.Column(db.String(50))
    fecha_viaje = db.Column(db.Date)
    hora_inicio = db.Column(db.DateTime)
    hora_final = db.Column(db.DateTime)
    estado_viaje = db.Column(db.String(30))
    ultima_ubicacion = db.Column(db.String(50))
    hora_ultimo = db.Column(db.DateTime)
    id_auto_viaje = db.Column(db.Integer)
    pasajeros = db.Column(db.Integer)
    id_tramo_viaje = db.Column(db.Integer)
    id_nivel_alerta = db.Column(db.Integer)
    estado_emb = db.Column(db.String(20))

    def __init__(self, origen,destino,fecha_viaje,hora_inicio,hora_final,estado_viaje,ultima_ubicacion,hora_ultimo,id_auto_viaje,pasajeros,id_tramo_viaje, id_nivel_alerta, estado_emb):
        self.origen = origen
        self.destino = destino
        self.fecha_viaje = fecha_viaje
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.estado_viaje = estado_viaje
        self.ultima_ubicacion = ultima_ubicacion
        self.hora_ultimo = hora_ultimo
        self.id_auto_viaje = id_auto_viaje
        self.pasajeros = pasajeros
        self.id_tramo_viaje = id_tramo_viaje
        self.id_nivel_alerta = id_nivel_alerta
        self.estado_emb = estado_emb

class Alertas_registradas(db.Model):
    id_registro = db.Column(db.Integer, primary_key=True)
    alerta_registrada = db.Column(db.Integer)
    id_viaje_alerta = db.Column(db.Integer)

    def __init__(self,alerta_registrada,id_viaje_alerta):
        self.alerta_registrada = alerta_registrada
        self.id_viaje_alerta = id_viaje_alerta