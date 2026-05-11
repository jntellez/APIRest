from pydantic import BaseModel, model_validator, Field
from datetime import datetime, timezone
from typing import List, Optional, Literal


class EventoCreate(BaseModel):
    nombre: str
    fechaInicio: datetime
    fechaFin: datetime
    cupo: int = Field(..., gt=0)
    # estatus:Optional[str]='Captura'
    descripcion: str
    tipo: str

    @model_validator(mode="after")
    def validarFechas(self):
        if self.fechaInicio > self.fechaFin:
            raise ValueError("La fecha de inicio debe ser menor o igual a la fecha fin")
        return self


class Salida(BaseModel):
    codigo: int
    mensaje: str


class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    cupo: Optional[int] = Field(None, gt=0)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None


class Evento(BaseModel):
    idEvento: str
    nombre: str
    fechaInicio: datetime
    fechaFin: datetime
    cupo: int
    estatus: str
    descripcion: str
    tipo: str
    fechaRegistro: datetime
    participantes: int


class EventoSalida(Salida):
    evento: Evento | None = None


class EventosSalida(Salida):
    eventos: List[Evento] | None = None


class EventoReprogramado(BaseModel):
    fechaInicio: datetime
    fechaFin: datetime
    motivo: Optional[str] = None
    # motivo:str|None=None

    @model_validator(mode="after")
    def validarFechas(self):
        fechaActual = datetime.now(timezone.utc)
        if self.fechaInicio > self.fechaFin and fechaActual <= self.fechaInicio:
            raise ValueError("Error en las fechas, favor de revisar el periodo.")
        return self


class CambioEstatus(BaseModel):
    idEvento: str
    estatus: Literal[
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
