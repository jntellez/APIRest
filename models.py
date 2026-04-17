from pydantic import BaseModel
from datetime import date
from typing import List


class EventoCreate(BaseModel):
    nombre: str
    fechaInicio: date
    fechaFin: date
    cupo: int
    estatus: str
    descripcion: str
    tipo: str


class Salida(BaseModel):
    codigo: int
    mensaje: str


class EventoUpdate(BaseModel):
    nombre: str
    cupo: int
    descripcion: str
    tipo: str


class ReprogramarEvento(BaseModel):
    fechaInicio: date
    fechaFin: date
    motivo: str


class Evento(BaseModel):
    idEvento: str
    nombre: str
    fechaInicio: date
    fechaFin: date
    cupo: int
    estatus: str
    descripcion: str
    tipo: str
    fechaRegistro: date
    inscritos: int


class EventoSalida(Salida):
    evento: Evento


class EventosSalida(Salida):
    eventos: List[Evento]
