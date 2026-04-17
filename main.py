from fastapi import FastAPI
import uvicorn
from datetime import date
from models import (
    EventoCreate,
    Salida,
    EventoUpdate,
    EventoSalida,
    Evento,
    EventosSalida,
    ReprogramarEvento,
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post(
    "/eventos",
    tags=["Eventos"],
    summary="Crear un evento",
    response_model=Salida,
)
def crearEvento(evento: EventoCreate) -> Salida:
    salida = Salida(codigo=200, mensaje="Evento creado")
    return salida


@app.get(
    "/eventos",
    tags=["Eventos"],
    summary="Listar eventos",
    response_model=EventosSalida,
)
def listarEventos() -> EventosSalida:
    evento = Evento(
        idEvento="123",
        nombre="Platica del Servicio Social",
        fechaInicio=date.today(),
        fechaFin=date.today(),
        cupo=100,
        estatus="Pendiente",
        descripcion="Descripcion",
        tipo="Platica",
        fechaRegistro=date.today(),
        inscritos=10,
    )

    salida = EventosSalida(
        codigo=200,
        mensaje="Eventos listados",
        eventos=[evento],
    )
    return salida


@app.get(
    "/eventos/{idEvento}",
    tags=["Eventos"],
    summary="Consultar evento por ID",
    response_model=EventoSalida,
)
def consultarEventoPorID(idEvento: str) -> EventoSalida:
    evento = Evento(
        idEvento=idEvento,
        nombre="Platica del Servicio Social",
        fechaInicio=date.today(),
        fechaFin=date.today(),
        cupo=100,
        estatus="Pendiente",
        descripcion="Descripcion",
        tipo="Platica",
        fechaRegistro=date.today(),
        inscritos=10,
    )

    salida = EventoSalida(
        codigo=200,
        mensaje=f"Evento con ID {idEvento} consultado",
        evento=evento,
    )
    return salida


@app.put(
    "/eventos/{idEvento}",
    tags=["Eventos"],
    summary="Modificar evento en base a su ID",
    response_model=Salida,
)
def modificarEvento(idEvento: str, evento: EventoUpdate) -> Salida:
    salida = Salida(codigo=200, mensaje=f"Evento con ID {idEvento} modificado")
    return salida


@app.get(
    "/eventos/estatus/{estatus}",
    tags=["Eventos"],
    summary="Consultar eventos por estatus",
    response_model=EventosSalida,
)
def consultarEventosPorEstatus(estatus: str) -> EventosSalida:
    evento = Evento(
        idEvento="123",
        nombre="Platica del Servicio Social",
        fechaInicio=date.today(),
        fechaFin=date.today(),
        cupo=100,
        estatus=estatus,
        descripcion="Descripcion",
        tipo="Platica",
        fechaRegistro=date.today(),
        inscritos=10,
    )

    salida = EventosSalida(
        codigo=200,
        mensaje=f"Eventos con estatus {estatus} consultados",
        eventos=[evento],
    )
    return salida


@app.put(
    "/eventos/estatus/{idEvento}/{estatus}",
    tags=["Eventos"],
    summary="Cambio de estatus de un evento",
    response_model=Salida,
)
def cambioEstatusEvento(idEvento: str, estatus: str) -> Salida:
    salida = Salida(
        codigo=200,
        mensaje=f"Cambio de estatus del evento con ID {idEvento} a {estatus}",
    )
    return salida


@app.put(
    "/eventos/reprogramar/{idEvento}",
    tags=["Eventos"],
    summary="Reprogramar evento",
    response_model=Salida,
)
def reprogramarEvento(idEvento: str, datos: ReprogramarEvento) -> Salida:
    salida = Salida(
        codigo=200,
        mensaje=(
            f"Evento con ID {idEvento} reprogramado del "
            f"{datos.fechaInicio} al {datos.fechaFin}"
        ),
    )
    return salida


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
