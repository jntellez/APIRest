from pymongo import MongoClient
from models import (
    EventoCreate,
    Salida,
    EventosSalida,
    EventoSalida,
    EventoUpdate,
    CambioEstatus,
    EventoReprogramado,
)
from datetime import datetime
from bson import ObjectId

DATABASEURL = "mongodb://localhost:27017/"
DATABASE = "EventosDB"


class Conexion:
    _cliente = None
    _db = None

    def __init__(self):
        try:
            self._cliente = MongoClient(DATABASEURL)
            self._db = self._cliente.EventosDB
            # self._db=self._cliente[DATABASE]
            print(f"Conectado con la BD: {DATABASE}")
        except Exception as ex:
            print(f"Error al conectar con la BD a causa de: {ex}")

    def cerrar(self):
        try:
            self._cliente.close()
            print(f"Conexion cerrada con la BD:{DATABASE}")
        except Exception as ex:
            print(f"Error al cerrar con la BD a causa de: {ex}")

    @property
    def db(self):
        return self._db


class EventoDAO:
    def __init__(self, db):
        self.db = db
        self.col = self.db.eventos
        self.view = self.db.eventosView

    def agregar(self, evento: EventoCreate):
        salida = Salida(codigo=0, mensaje="")
        try:
            data = evento.model_dump()
            data["fechaRegistro"] = datetime.today()
            data["estatus"] = "Captura"
            data["participantes"] = 0
            result = self.col.insert_one(data)
            salida.codigo = 201
            salida.mensaje = "Evento creado exitosamente con id:" + str(
                result.inserted_id
            )
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error:{ex}"
        return salida

    def consultaGeneral(self):
        salida = EventosSalida(codigo=200, mensaje="", eventos=[])
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de eventos"
            salida.eventos = list(self.view.find({}, {"_id": 0}))
        except Exception as ex:
            salida.codigo = 404
            salida.mensaje = f"Error al consultar los eventos,{ex}"
        return salida

    def consultaPorID(self, idEvento: str):
        salida = EventoSalida(codigo=0, mensaje="", evento=None)
        try:
            salida.codigo = 200
            salida.mensaje = "Listado del evento"
            salida.evento = self.view.find_one({"idEvento": idEvento}, {"_id": 0})
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error:{ex}"
        return salida

    def consultaPorEstatus(self, estatus):
        salida = EventosSalida(codigo=0, mensaje="", eventos=[])
        estatus_permitidos = [
            "Captura",
            "Revision",
            "Rechazado",
            "Autorizado",
            "Cancelado",
            "Planeacion",
            "Difusion",
            "Pospuesto",
            "Proceso",
            "Finalizado",
        ]
        if estatus not in estatus_permitidos:
            salida = EventosSalida(
                codigo=404, mensaje="El estatus no es un valor permitido.", eventos=None
            )
        else:
            try:
                salida.codigo = 200
                salida.mensaje = "Listado de eventos"
                salida.eventos = list(self.view.find({"estatus": estatus}, {"_id": 0}))
            except Exception as ex:
                salida.codigo = 500
                salida.mensaje = f"Error al consultar los eventos:{ex}"
        return salida

    def cambiarEstatus(self, idEvento: str, estatus: str) -> Salida:
        salida = Salida(codigo=0, mensaje="")

        transiciones_permitidas = {
            "Captura": ["Revision"],
            "Revision": ["Rechazado", "Cancelado", "Autorizado"],
            "Rechazado": ["Captura"],
            "Autorizado": ["Planeacion"],
            "Planeacion": ["Difusion", "Pospuesto"],
            "Pospuesto": ["Difusion"],
            "Difusion": ["Proceso"],
            "Proceso": ["Cancelado", "Finalizado"],
        }

        estatus_permitidos = [
            "Captura",
            "Revision",
            "Rechazado",
            "Autorizado",
            "Cancelado",
            "Planeacion",
            "Difusion",
            "Pospuesto",
            "Proceso",
            "Finalizado",
        ]

        if estatus not in estatus_permitidos:
            salida.codigo = 404
            salida.mensaje = "El estatus no es un valor permitido."
            return salida

        if not ObjectId.is_valid(idEvento):
            salida.codigo = 404
            salida.mensaje = f"El id del evento:{idEvento} no es valido."
            return salida

        try:
            evento = self.col.find_one({"_id": ObjectId(idEvento)})
            if not evento:
                salida.codigo = 404
                salida.mensaje = f"El evento con id:{idEvento} no existe."
                return salida

            estatus_actual = evento.get("estatus")
            siguiente_estatus = transiciones_permitidas.get(estatus_actual, [])
            if estatus not in siguiente_estatus:
                salida.codigo = 404
                salida.mensaje = (
                    f"No es posible cambiar del estatus {estatus_actual} al estatus {estatus}."
                )
                return salida

            result = self.col.update_one(
                {"_id": ObjectId(idEvento)}, {"$set": {"estatus": estatus}}
            )
            if result.modified_count > 0:
                salida.codigo = 200
                salida.mensaje = (
                    f"El estatus del evento con id:{idEvento} cambio a {estatus} exitosamente."
                )
            else:
                salida.codigo = 500
                salida.mensaje = "No fue posible cambiar el estatus del evento."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error:{ex}"

        return salida

    def modificar(self, evento: EventoUpdate, idEvento: str):
        eventoRec = self.view.find_one({"idEvento": idEvento})
        salida = Salida(codigo=0, mensaje="")
        if eventoRec:
            data = evento.model_dump(exclude_unset=True)
            result = None
            if eventoRec["estatus"] == "Captura":
                if data.keys():
                    result = self.col.update_one(
                        {"_id": ObjectId(idEvento)}, {"$set": data}
                    )
                else:
                    salida.codigo = 500
                    salida.mensaje = "Debes proporcionar un valor a modificar."
            elif eventoRec["estatus"] == "Difusion" and data.__contains__("cupo"):
                result = self.col.update_one(
                    {"_id": ObjectId(idEvento)}, {"$set": {"cupo": data["cupo"]}}
                )
            if result != None and result.modified_count > 0:
                salida.codigo = 200
                salida.mensaje = f"El evento con id:{idEvento} se modifico con exito."
            else:
                salida.codigo = 404
                salida.mensaje = "El estatus del evento no es Captura o Difusion."
        else:
            salida.codigo = 404
            salida.mensaje = f"El evento con id:{idEvento} no existe."
        return salida

    def reprogramar(self, idEvento, evento: EventoReprogramado):
        respuesta = self.consultaPorID(idEvento)
        salida = Salida(codigo=0, mensaje="")
        if respuesta.codigo == 200:
            if respuesta.evento["estatus"] == "Planeacion":
                data = evento.model_dump(exclude_unset=True)
                result = self.col.update_one(
                    {"_id": ObjectId(idEvento)}, {"$set": data}
                )
                if result.modified_count > 0:
                    salida.codigo = 200
                    salida.mensaje = (
                        f"Evento con id:{idEvento} reprogramado exitosamente."
                    )
                else:
                    salida.codigo = 500
                    salida.mensaje = (
                        "El evento no existe o no se pudo reprogramar con exito"
                    )
            else:
                salida.codigo = 404
                salida.mensaje = (
                    "El evento no se encuentra en planeación para su reprogramación."
                )
        else:
            salida.codigo = 404
            salida.mensaje = f"El evento con id:{idEvento} no existe."
        return salida

    def eliminar(self, idEvento: str) -> Salida:
        salida = Salida(codigo=0, mensaje="")

        if not ObjectId.is_valid(idEvento):
            salida.codigo = 404
            salida.mensaje = f"El id del evento:{idEvento} no es valido."
            return salida

        try:
            evento = self.col.find_one({"_id": ObjectId(idEvento)})
            if not evento:
                salida.codigo = 404
                salida.mensaje = f"El evento con id:{idEvento} no existe."
                return salida

            if evento.get("estatus") != "Cancelado":
                salida.codigo = 404
                salida.mensaje = (
                    "El evento no se puede eliminar porque su estatus no es Cancelado."
                )
                return salida

            result = self.col.delete_one({"_id": ObjectId(idEvento)})
            if result.deleted_count > 0:
                salida.codigo = 200
                salida.mensaje = f"Evento con id:{idEvento} eliminado exitosamente."
            else:
                salida.codigo = 500
                salida.mensaje = "No fue posible eliminar el evento."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error:{ex}"

        return salida
