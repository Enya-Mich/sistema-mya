from app import db

class Sindicato(db.Model):
    id_sindicato = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    ubicacion = db.Column(db.String(50))
    id_municipio = db.Column(db.Integer)

    def __init__(self, nombre, ubicacion, id_municipio):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.id_municipio = id_municipio


class Telefonos_sindicato(db.Model):
    id_telefono = db.Column(db.Integer, primary_key=True)
    numero_telefono = db.Column(db.Integer)
    id_sindicato = db.Column(db.Integer)
    propietario = db.Column(db.String(50))

    def __init__(self, numero_telefono, id_sindicato, propietario):
        self.numero_telefono = numero_telefono
        self.id_sindicato = id_sindicato
        self.propietario = propietario

class Autos(db.Model):
    id_auto = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(8))
    tiempo_cambio_llanta = db.Column(db.Integer)
    marca = db.Column(db.String(20))
    color = db.Column(db.String(20))
    id_chofer = db.Column(db.Integer)

    def __init__(self, placa, tiempo_cambio_llanta, marca, color, id_chofer):
        self.placa = placa
        self.tiempo_cambio_llanta = tiempo_cambio_llanta
        self.marca = marca
        self.color = color
        self.id_chofer = id_chofer