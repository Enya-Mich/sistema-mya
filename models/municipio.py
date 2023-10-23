from app import db

class Municipio(db.Model):
    id_municipio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    ubicacion = db.Column(db.String(50))

    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion


class Telefonos_municipio(db.Model):
    id_telefono_m = db.Column(db.Integer, primary_key=True)
    numero_telefono = db.Column(db.Integer)
    id_municipio = db.Column(db.Integer)
    propietario = db.Column(db.String(50))

    def __init__(self, numero_telefono, id_municipio, propietario):
        self.numero_telefono = numero_telefono
        self.id_municipio = id_municipio
        self.propietario = propietario


class Tramos(db.Model):
    id_tramo = db.Column(db.Integer, primary_key=True)
    km_inicio = db.Column(db.String(50))
    km_final = db.Column(db.String(50))
    zona_riesgosa = db.Column(db.Integer)
    tiempo_ida = db.Column(db.Integer)
    señal_internet = db.Column(db.Integer)
    señal_normal = db.Column(db.Integer)
    id_municipio = db.Column(db.Integer)

    def __init__(self ,km_inicio ,km_final ,zona_riesgosa,tiempo_ida,señal_internet,señal_normal,id_municipio):
        self.km_inicio = km_inicio
        self.km_final = km_final
        self.zona_riesgosa = zona_riesgosa
        self.tiempo_ida = tiempo_ida
        self.señal_internet = señal_internet
        self.señal_normal = señal_normal
        self.id_municipio = id_municipio