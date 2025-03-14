from motor.motor_asyncio import AsyncIOMotorClient
from enum import Enum


class Collection(str, Enum):
    STUDENTS = "alumnos"
    TOPICS = "asignaturas"
    RECORDS = "historial"
    LOADS = "cargas"


def get_collection(coll: str):
    client = AsyncIOMotorClient("mongodb://127.0.0.1:27017")
    return client["cobach217"][coll]
