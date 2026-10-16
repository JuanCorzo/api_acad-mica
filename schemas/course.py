from pydantic import BaseModel, Field


# Esquema de entrada: valida el cuerpo JSON antes de ejecutar el endpoint.
class CourseCreate(BaseModel):
    # El nombre debe tener entre 3 y 80 caracteres.
    name: str = Field(min_length=3, max_length=80)
    # Solo se admiten cursos con entre 1 y 6 créditos.
    credits: int = Field(ge=1, le=6)
    active: bool = True


# Esquema de actualización completa: los tres campos son obligatorios.
class CourseUpdate(BaseModel):
    # El nombre debe tener entre 3 y 80 caracteres.
    name: str = Field(min_length=3, max_length=80)
    # Solo se admiten cursos con entre 1 y 6 créditos.
    credits: int = Field(ge=1, le=6)
    # Sin valor predeterminado: omitir active produce 422.
    active: bool


# Esquema de salida: define los campos devueltos al cliente, incluido el ID.
class CourseResponse(BaseModel):
    id: int
    name: str
    credits: int
    active: bool
