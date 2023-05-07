# import os
# from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy.sql import func




# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# db = SQLAlchemy()




# # def create_app():
# #     """Construct the core application."""
# #     app = Flask(__name__, instance_relative_config=False)
# #     app.config.from_object('config.Config')

# #     db.init_app(app)

# #     with app.app_context():
# #         from . import routes  # Import routes
# #         db.create_all()  # Create sql tables for our data models

# #         return app

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()
app = Flask(__name__)

# Configure MariaDB connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"

 # Create SQLAlchemy object
db = SQLAlchemy(app)
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

with app.app_context():
    db.create_all()

@app.route("/users",methods=["GET"])
def fetch_users():
     # Query the database
    data = User.query.all()

    # Convert the data to a dictionary
    data_dict = [row.__dict__ for row in data]

    # Remove the "_sa_instance_state" key from each dictionary
    for row in data_dict:
        row.pop('_sa_instance_state', None)

    return str(data_dict)

@app.route("/users", methods=["POST"])
def create_user():
    # Example POST data format: {"nombre": "John", "apellidoMaterno": "Doe", ...}
    data = request.get_json()
    fecha_nacimiento = datetime.strptime(data['fechaNacimiento'], '%Y-%m-%d %H:%M:%S')
    new_user = User(
        nombre=data["nombre"],
        apellidoMaterno=data["apellidoMaterno"],
        apellidoPaterno=data["apellidoPaterno"],
        cargo=data["cargo"],
        empresa=data["empresa"],
        calle=data["calle"],
        numeroExt=data["numeroExt"],
        numeroInt=data["numeroInt"],
        colonia=data["colonia"],
        municipio=data["municipio"],
        estado=data["estado"],
        codigoPostal=data["codigoPostal"],
        telefono=data["telefono"],
        correoElectronico=data["correoElectronico"],
        fechaNacimiento=fecha_nacimiento
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"user": "User created successfully!"}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state', None)
        return jsonify(user_dict)
    else:
        return jsonify({"message": "User not found."}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Query the database for the user to update
    user = User.query.get(user_id)

    # Check if the user exists
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Update the user fields with the request body data
    if 'nombre' in request.json:
        user.nombre = request.json['nombre']
    if 'apellidoMaterno' in request.json:
        user.apellidoMaterno = request.json['apellidoMaterno']
    if 'apellidoPaterno' in request.json:
        user.apellidoPaterno = request.json['apellidoPaterno']
    if 'cargo' in request.json:
        user.cargo = request.json['cargo']
    if 'empresa' in request.json:
        user.empresa = request.json['empresa']
    if 'calle' in request.json:
        user.calle = request.json['calle']
    if 'numeroExt' in request.json:
        user.numeroExt = request.json['numeroExt']
    if 'numeroInt' in request.json:
        user.numeroInt = request.json['numeroInt']
    if 'colonia' in request.json:
        user.colonia = request.json['colonia']
    if 'municipio' in request.json:
        user.municipio = request.json['municipio']
    if 'estado' in request.json:
        user.estado = request.json['estado']
    if 'codigoPostal' in request.json:
        user.codigoPostal = request.json['codigoPostal']
    if 'telefono' in request.json:
        user.telefono = request.json['telefono']
    if 'correoElectronico' in request.json:
        user.correoElectronico = request.json['correoElectronico']
    if 'fechaNacimiento' in request.json:
        fecha_nacimiento = datetime.strptime(request.json['fechaNacimiento'], '%Y-%m-%d %H:%M:%S')
        user.fechaNacimiento = fecha_nacimiento
  
    # Save the changes to the database
    db.session.commit()
    print("hola")
    print("adios")
    # Return the updated user as JSON

    user_dict = user.__dict__
    user_dict.pop('_sa_instance_state', None)
    return jsonify(user_dict)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    else:
        return jsonify({"message": "User not found."}), 404
