from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/eventos", tags=["Eventos"], summary="Crear un evento")
def crearEvento():
    return {"message": "Evento creado"}


@app.get("/eventos", tags=["Eventos"], summary="Listar eventos")
def listarEventos():
    return {"message": "Eventos listados"}


@app.get("/eventos/{idEvento}", tags=["Eventos"], summary="Consultar evento por ID")
def consultarEventoPorID(idEvento: str):
    return {"message": f"Evento con ID {idEvento} consultado"}


@app.put(
    "/eventos/{idEvento}", tags=["Eventos"], summary="Modificar evento en base a su ID"
)
def modificarEvento(idEvento: str):
    return {"message": f"Evento con ID {idEvento} modificado"}


@app.get(
    "/eventos/estatus/{estatus}",
    tags=["Eventos"],
    summary="Consultar eventos por estatus",
)
def consultarEventosPorEstatus(estatus: str):
    return {"message": f"Eventos con estatus {estatus} consultados"}


@app.put(
    "/eventos/estatus/{idEvento}",
    tags=["Eventos"],
    summary="Cambio de estatus de un evento",
)
def cambioEstatusEvento(idEvento: str):
    return {"message": f"Cambio de estatus de un evento con ID {idEvento}"}


@app.put(
    "/eventos/reprogramar/{idEvento}", tags=["Eventos"], summary="Reprogramar evento"
)
def reprogramarEvento(idEvento: str):
    return {"message": f"Evento con ID {idEvento} reprogramado"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
