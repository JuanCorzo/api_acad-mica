from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    email: str = Field(min_length=1)
    semester: int = Field(ge=1, le=10)
    active: bool = True


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    semester: int
    active: bool
