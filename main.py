from fastapi import FastAPI, Request
from models import (
    EventoCreate,
    Salida,
    EventoUpdate,
    EventoSalida,
    EventosSalida,
    EventoReprogramado,
    CambioEstatus,
)
import uvicorn
from dao import Conexion, EventoDAO

app = FastAPI()


@app.get("/", tags=["Inicio"], summary="Home")
def home():
    return "Bienvenido a la APIRest de Eventos"


@app.post("/eventos", tags=["Eventos"], summary="Crear Evento", response_model=Salida)
async def crearEvento(request: Request, evento: EventoCreate) -> Salida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.agregar(evento)


@app.get(
    "/eventos", tags=["Eventos"], summary="Listar Eventos", response_model=EventosSalida
)
async def listarEventos(request: Request) -> EventosSalida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.consultaGeneral()


@app.get(
    "/eventos/{idEvento}",
    tags=["Eventos"],
    summary="Listar Evento",
    response_model=EventoSalida,
)
def listarEvento(request: Request, idEvento: str) -> EventoSalida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.consultaPorID(idEvento)


@app.put(
    "/eventos/{idEvento}",
    tags=["Eventos"],
    summary="Modificar evento en base a su ID",
    response_model=Salida,
)
def modificarEvento(request: Request, idEvento: str, evento: EventoUpdate) -> Salida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.modificar(evento, idEvento)


@app.get(
    "/eventos/estatus/{estatus}",
    tags=["Eventos"],
    summary="Consultar eventos pos estatus",
    response_model=EventosSalida,
)
def consultarEventosPorEstatus(request: Request, estatus: str) -> EventosSalida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.consultaPorEstatus(estatus)


@app.put(
    "/eventos/estatus/{idEvento}/{estatus}",
    tags=["Eventos"],
    summary="Cambio de estatus de un evento",
    response_model=Salida,
)
def cambioEstatusEvento(request: Request, idEvento: str, estatus: str) -> Salida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.cambiarEstatus(idEvento, estatus)


@app.put(
    "/eventos/reprogramar/{idEvento}",
    tags=["Eventos"],
    summary="Reprogramar Evento",
    response_model=Salida,
)
def reprogramarEvento(request: Request, idEvento: str, evento: EventoReprogramado):
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.reprogramar(idEvento, evento)


@app.delete(
    "/eventos/{idEvento}",
    tags=["Eventos"],
    summary="Eliminar Evento",
    response_model=Salida,
)
def eliminarEvento(request: Request, idEvento: str) -> Salida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.eliminar(idEvento)


@app.on_event("startup")
def startup():
    conexion = Conexion()
    app.cn = conexion


@app.on_event("shutdown")
def shutdown():
    app.cn.cerrar()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
