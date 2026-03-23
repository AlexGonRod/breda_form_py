from pydantic import BaseModel, Field

class FORMDATA(BaseModel):
    nom: str = Field(..., min_length=1)
    telefon: str = Field(..., min_length=9, max_length=9)
    persones: str = Field(..., pattern="^([1-9]|[1-3][0-9]|40)$")
