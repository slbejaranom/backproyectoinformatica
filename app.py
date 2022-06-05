from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

class Receta(db.Model):
    id = db.Column("id_receta", db.Integer, primary_key = True)
    descripcion = db.Column("descripcion", db.Text)
    enPedidos = db.relationship("PedidoReceta", backref="receta")

    def __init__(self, receta):
        self.id = receta["id"]
        self.descripcion = receta["descripcion"]

class PedidoReceta(db.Model):
    idItem = db.Column("id_item_pedido", db.Integer, primary_key = True) 
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"))
    receta_id = db.Column(db.Integer, db.ForeignKey("receta.id"))

db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)

#Obtener todos los pedidos
@app.route("/pedidos", methods=["GET"])
def obtenerPedidos():
    pedidos = Pedido.query.all()
    if(pedidos):
        return pedidos, 200
    else:
        return "No hay pedidos", 404

#Obtener pedido por id
@app.route("/pedidos/<id>")
def obtenerPedidoPorId(id):
    pedido = Pedido.query.filter(id = id)
    if(pedido):
        return pedido, 200
    else:
        return "No hay pedido con ese ID", 404