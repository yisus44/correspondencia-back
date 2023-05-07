import os
from flask import Blueprint, jsonify, request, Response, send_file
from models import User
from datetime import datetime
from app import db
from reportlab.pdfgen import canvas
from flask_cors import cross_origin


user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/users",methods=["GET"])
@cross_origin()
def fetch_users():
     # Query the database
    data = User.query.all()

    # Convert the data to a dictionary
    data_dict = [row.__dict__ for row in data]

    # Remove the "_sa_instance_state" key from each dictionary
    for row in data_dict:
        row.pop('_sa_instance_state', None)

    return jsonify(data_dict)

@user_routes.route("/users", methods=["POST"])
@cross_origin()
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

@user_routes.route("/users/<int:user_id>", methods=["GET"])
@cross_origin()
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state', None)
        return jsonify(user_dict)
    else:
        return jsonify({"message": "User not found."}), 404

def generate_user_report(user_dict):
    # Define the folder path for the output files
    output_folder_path = "output"
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
   
    # Define the canvas for the PDF
    c = canvas.Canvas(os.path.join(output_folder_path, f"{user_dict['nombre']}_{user_dict['apellidoMaterno']}_{user_dict['apellidoPaterno']}.pdf"))
   
    # Define the template file path and read its contents
    template_file_path = "template.txt"
    with open(template_file_path, "r") as template_file:
        template_content = template_file.read()
   
    # Replace placeholders in the template with user data
    for key, value in user_dict.items():
        template_content = template_content.replace("{" + key + "}", str(value))

    # Split the template content into lines
    lines = template_content.split("\n")
   
    # Define the starting y-coordinate for the text
    y = 750
   
    # Draw each line of the template on the canvas
    for line in lines:
        c.drawString(100, y, line)
        y -= 20 # Move down by 20 units for each line
   
    # Save the PDF
    c.showPage()
    c.save()


@user_routes.route("/users/invitations/<int:user_id>", methods=["GET"])
@cross_origin()
def get_user_invitations(user_id):
    user = User.query.get(user_id)
    if user:
        # Delete files
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state', None)
        # Calculate age
        nacimiento = user_dict["fechaNacimiento"].strftime("%Y-%m-%d")
        user_dict["fechaNacimiento"]= user_dict["fechaNacimiento"].strftime('%Y-%m-%d')
        edad = 2023 - int(nacimiento[:4])
        user_dict["edadCalculada"] = edad
        # Generate report
        generate_user_report(user_dict)
        
        # Return the PDF file
        pdf_file_path = os.path.join("output", f"{user_dict['nombre']}_{user_dict['apellidoMaterno']}_{user_dict['apellidoPaterno']}.pdf")
        return send_file(pdf_file_path, download_name=f"{user_dict['nombre']}_{user_dict['apellidoMaterno']}_{user_dict['apellidoPaterno']}.pdf", as_attachment=True)
    
    return jsonify({'message': 'User not found'})

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
@cross_origin()
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


@user_routes.route("/users/<int:user_id>", methods=["DELETE"])
@cross_origin()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    else:
        return jsonify({"message": "User not found."}), 404
