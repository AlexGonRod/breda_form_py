from pydantic import BaseModel

class FORMDATA(BaseModel):
    nombre: str
    telefon: int
    persones: int
