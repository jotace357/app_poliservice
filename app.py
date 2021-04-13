from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

from Usuarios import Usuarios
from reservas import reservas
from Servicios import Servicios

# solo ping para saber si responde la url y el servicio
@app.route('/ping', methods=['GET'])
def ping():
    print("llamada a ping (/ping)")
    return jsonify({"message":"pong!"})


# login se le pasa los parametros dni y password
# 
""" @app.route('/appiniciarsesion',  methods=['POST'])
def login():
    print("llamada a login (/appiniciarsesion)")
    aleluya = request.json['dni']
    aleluya1 = request.json['password']
    print("request.json['dni']="+aleluya)
    print("request.json['password']="+aleluya1)
    usuarioEncontrado = [usu for usu in Usuarios if usu['dni']==request.json['dni'] and usu['password']==request.json['password']]
    if (len(usuarioEncontrado) > 0):
        print("entre en el if")
        return jsonify({"cod_retorno": "00", "detalle":"Proceso ok", "Usuario": usuarioEncontrado})
    return jsonify({"cod_retorno": "01", "detalle":"Dni usuario o clave incorrectos" })

 """

# adaptación a la manera de Emiliano de esta forma no toma json como entrada, sino como request del formulario, y el json de salida esta armado a mano
@app.route("/appiniciarsesion", methods=["POST"])
def appiniciarsesion():
	if request.method == "POST":
		
		#user = usuarios.query.filter_by(dni= request.form["dni_init"]).first()
		usuarioEncontrado = [usu for usu in Usuarios if usu['dni']==request.form["dni_init"] and usu['password']==request.form["pass_init"]]  
		if (len(usuarioEncontrado) > 0):
			#login_user(user)
			
			#print(request.form["dni_init"])
			#print(request.form["pass_init"])
			#return ("BIENVENIDO A POLISOFT")
			return jsonify({"id": usuarioEncontrado[0]['id'],
							"username":usuarioEncontrado[0]['username'],
							"lastname": usuarioEncontrado[0]['lastname'],
							"dni": usuarioEncontrado[0]['dni'],
							"address": usuarioEncontrado[0]['address'],
							"movilphone":usuarioEncontrado[0]['movilphone'],
							"phone": usuarioEncontrado[0]['phone'],
							"email": usuarioEncontrado[0]['email']})

		return jsonify({"detalle":" * Los datos ingresados son incorrectos, intente nuevamente", "cod_retorno":"01"})

# addUsuarios metodo post parametros username, lastname, dni, address, movilphone, phone, email password,emergency
@app.route('/addUsuario', methods=['POST'])
def addUsuarios():
    print("llamada a addUsuarios (/addUsuarios)")
    idusuario = len(Usuarios) + 1
    #print ("usuarios encontrados" + str(usuariosEncontrados))
    new_usuario = {
        "id":idusuario,
        "username":request.json['username'],
        "lastname":request.json['lastname'],
        "dni":request.json['dni'],
        "address":request.json['address'],
        "movilphone":request.json['movilphone'],
        "phone":request.json['phone'],
        "email":request.json['email'],
        "password":request.json['password'],
        "emergency":request.json['emergency']
    }
    Usuarios.append(new_usuario)
    nuevousuario = [usu for usu in Usuarios if usu['id']==idusuario]
    return jsonify({"cod_retorno": "00", "detalle":"Proceso ok", "Nuevo Usuario": nuevousuario})

# Usuarios, devuelve todos los usuarios metodo get
@app.route('/Usuarios', methods=['GET'])
def getUsuarios():
    print("llamada a getUsuarios (/Usuarios)")
    return jsonify({"usuarios": Usuarios, "cod_retorno":"00" ,"detalle":"Proceso Ok"})

# editar usuario
@app.route('/editUsuario/<string:usuario_dni>', methods=['PUT'])
def editUsuarios(usuario_dni):
    print("llamada a editUsuarios (/editUsuarios) parametro: dni "+usuario_dni)
    usuarioEncontrado = [usu for usu in Usuarios if usu['dni']==usuario_dni]
    if(len(usuarioEncontrado) > 0):
        usuarioEncontrado[0]['username'] = request.json['username']
        usuarioEncontrado[0]['lastname'] = request.json['lastname']
        usuarioEncontrado[0]['address'] = request.json['address']
        usuarioEncontrado[0]['movilphone'] = request.json['movilphone']
        usuarioEncontrado[0]['phone'] = request.json['phone']
        usuarioEncontrado[0]['email'] = request.json['email']
        usuarioEncontrado[0]['password'] = request.json['password']
        usuarioEncontrado[0]['emergency'] = request.json['emergency']
        return jsonify({"usuario": usuarioEncontrado, "cod_retorno":"00" ,"detalle":"Proceso Ok"}) 
    return jsonify({"cod_retorno":"01" ,"detalle":"No se encontro usuario"})


# Devuelve los servicios segun policlinica, esencialidad y medico
@app.route('/Servicios/<string:policlinica>/<string:especialidad>/<string:medico>', methods=['GET'])
def getServicios(policlinica, especialidad, medico ):
    print("llamada a getServicios (/Servicios) parametros:policlinica: "+policlinica+ " especialidad "+especialidad+ " medico "+medico)
    
    servicioEncontrados = [ serv for serv in Servicios ]

    if not (policlinica == None):
        servicioEncontrados =[ serv for serv in servicioEncontrados if serv['policlinica']==policlinica ]
    
    if not (especialidad == None):
        servicioEncontrados =[ serv for serv in servicioEncontrados if serv['especialidad']==especialidad ]
    
    if not (medico == None):
        servicioEncontrados =[ serv for serv in servicioEncontrados if serv['nombre']==medico ]
    
    return jsonify({"Servicios": servicioEncontrados,"cod_retorno":"00" ,"detalle":"Proceso Ok"})


@app.route('/addReservas', methods=['POST'])
def addReservas():
    print("llamada a addReservas (/addReservas) parametros: user_id ")
    idr = len(reservas) + 1
    numturnos = len(reservas[3]) + 1
    print ("numturnos =" + str(numturnos))
    new_reserv = {
        "id":idr,
        "atencion":request.json['atencion'],
        "numturnos":numturnos,
        "user_id":request.json['idusuario']
    }
    reservas.append(new_reserv)
    nuevareserva = [res for res in reservas if res['id']==idr]
    return jsonify({"cod_retorno": "00", "detalle":"Proceso ok", "Reserva": nuevareserva})

@app.route('/consultaReservas/<int:idusuario>', methods=['GET'])
def getReservaUsuario(idusuario):
    print("llamada a getReservaUsuario (/consultaReservas) parametros: user_id "+ str(idusuario))
    reservasFound = [rese for rese in reservas if rese['user_id'] == idusuario]
    print("lpase1")
    
    servFound = [ser for ser in Servicios if ser['id'] == reservasFound[0]['atencion']]
    #print("pase 2")
    resultado =[ np.hstack((reservasFound, servFound)) ]
    print("resultado"+str(resultado))
    return jsonify({"Reservas": reservasFound,"Servicios": servFound, "cod_retorno":"00" ,"detalle":"Proceso Ok"})

if __name__ == '__main__':
    #app.run(host="192.168.1.2", port=4000,debug=True)
    app.run(host="0.0.0.0", port=4000,debug=True)
    