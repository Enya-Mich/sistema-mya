from app import db

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol_usuario = db.Column(db.Integer)
    ci_usuario = db.Column(db.Integer)

    def __init__(self, nombre_usuario, contrasena, rol_usuario, ci_usuario):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol_usuario = rol_usuario
        self.ci_usuario = ci_usuario

class Persona(db.Model):
    ci = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    telefono = db.Column(db.Integer)
    rol_sindicato = db.Column(db.String(30))
    id_sindicato = db.Column(db.Integer)

    def __init__(self, ci, nombre, telefono, rol_sindicato, id_sindicato):
        self.ci = ci
        self.nombre = nombre
        self.telefono = telefono
        self.rol_sindicato = rol_sindicato
        self.id_sindicato = id_sindicato