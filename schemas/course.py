from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)
    active: bool = True


class CourseUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)
    active: bool


class CourseResponse(BaseModel):
    id: int
    name: str
    credits: int
    active: bool
