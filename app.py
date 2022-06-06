from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import sys
from flask_cors import CORS
from sqlalchemy import JSON

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://informatica:informatica@mysql/informatica'
db = SQLAlchemy(app)

class Pedido(db.Model):
    id = db.Column("id_pedido",db.Integer, primary_key = True)
    numPersonas = db.Column("num_personas",db.Integer)
    cantRecetasSemana = db.Column("cant_recetas_semana",db.Integer)
    correo = db.Column("correo", db.Text)
    nombre = db.Column("nombre", db.Text)
    apellido = db.Column("apellido", db.Text)
    direccion = db.Column("direccion", db.Text)
    telefono = db.Column("telefono", db.Text)
    total = db.Column("total", db.Float)
    numTarjeta = db.Column("num_tarjeta", db.Text)
    cvv = db.Column("cvv", db.Text)
    expiracion = db.Column("expiracion", db.Text)
    itemsPedido = db.relationship("PedidoReceta", backref="pedido")

    def __init__(self, pedido):
        self.id = pedido["id"]
        self.numPersonas = pedido["numPersonas"]
        self.cantRecetasSemana = pedido["cantRecetasSemana"]
        self.correo = pedido["correo"]
        self.nombre = pedido["nombre"]
        self.apellido = pedido["apellido"]
        self.direccion = pedido["direccion"]
        self.telefono = pedido["telefono"]
        self.total = pedido["total"]
        self.numTarjeta = pedido["numTarjeta"]
        self.cvv = pedido["cvv"]
        self.expiracion = pedido["expiracion"]
        self.itemsPedido = pedido["itemsPedido"]
    
    def asDict(self):
        return {
            "id" : self.id,
            "numPersonas" : self.numPersonas,
            "cantRecetasSemana" : self.cantRecetasSemana,
            "correo" : self.correo,
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "direccion" : self.direccion,
            "telefono" : self.telefono,
            "total" : self.total,
            "numTarjeta" : self.numTarjeta,
            "cvv" : self.cvv,
            "expiracion" : self.expiracion,
            "itemsPedido": self.itemsPedido
        }

class Receta(db.Model):
    id = db.Column("id_receta", db.Integer, primary_key = True)
    descripcion = db.Column("descripcion", db.Text)
    urlImagen = db.Column("url_imagen", db.Text)
    enPedidos = db.relationship("PedidoReceta", backref="receta")

    def __init__(self, receta):
        self.id = receta["id"]
        self.descripcion = receta["descripcion"]
        self.urlImagen = receta["urlImagen"]

class PedidoReceta(db.Model):
    idItem = db.Column("id_item_pedido", db.Integer, primary_key = True) 
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id_pedido"))
    receta_id = db.Column(db.Integer, db.ForeignKey("receta.id_receta"))

db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)

#Obtener todos los pedidos
@app.route("/pedidos", methods=["GET"])
def obtenerPedidos():
    pedidos = Pedido.query.all()
    if(pedidos):
        return json.dumps(list(map(lambda pedido : pedido.asDict(), pedidos))), 200
    else:
        return "No hay pedidos", 404

#Obtener pedido por id
@app.route("/pedidos/<id>", methods=["GET"])
def obtenerPedidoPorId(id):
    pedido = Pedido.query.filter_by(id = id).first()
    if(pedido):
        return json.dumps(pedido.asDict()), 200
    else:
        return "No hay pedido con ese ID", 404

#Agregar nuevo pedido
@app.route("/pedidos", methods=["POST"])
def agregarPedido():    
    data = json.loads(request.data)
    print(data, file=sys.stderr)
    try:
        pedido = Pedido(data)
        print(pedido, file=sys.stderr)
        db.session.add(pedido)
        db.session.commit()
        return json.dumps(pedido.asDict()), 200
    except Exception as ex:
        return "Verifique que todos los campos cumplan con la descripción", 400

#Modificar pedido
@app.route("/pedidos/<id>", methods=["PUT"])
def modificarPedido(id):
    data = json.loads(request.data)
    pedido = Pedido.query.filter_by(id=id).first()
    if(pedido):
        try:
            pedido = Pedido(data)
            db.session.commit()
            return json.dumps(pedido.asDict()),200
        except Exception as ex:
            return "Verifique que todos los campos cumplan con la descripción", 400
    else:
        return "No hay pedido con ese ID", 404
