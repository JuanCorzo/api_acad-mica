from sqlmodel import SQLModel, Field


# table=True convierte este modelo en una tabla administrada por SQLModel.
class Student(SQLModel, table=True):

    # La clave primaria identifica al estudiante; SQLite la asigna al insertarlo.
    id: int | None = Field(
        default=None,
        primary_key=True
    )

    # Los campos tipados definen las columnas de la tabla.
    name: str

    email: str

    semester: int

    # Un estudiante nuevo queda activo si no se indica otro valor.
    active: bool = True
