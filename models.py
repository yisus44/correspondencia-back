from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidoMaterno = db.Column(db.String(50))
    apellidoPaterno = db.Column(db.String(50))
    cargo = db.Column(db.String(25))
    empresa = db.Column(db.String(25))
    calle = db.Column(db.String(40))
    numeroExt = db.Column(db.String(10))
    numeroInt = db.Column(db.String(10))
    colonia = db.Column(db.String(25))
    municipio = db.Column(db.String(25))
    estado = db.Column(db.String(25))
    codigoPostal = db.Column(db.String(10))
    telefono = db.Column(db.String(10)) 
    correoElectronico = db.Column(db.String(256)) 
    fechaNacimiento = db.Column(db.DateTime) 
    def __repr__(self):
        return '<User {}>'.format(self.nombre)