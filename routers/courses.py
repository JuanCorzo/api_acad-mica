from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_session
from schemas.course import CourseCreate, CourseResponse

from services.course_service import (
    create_course,
    list_courses,
    get_course
)


# Agrupa las rutas bajo /courses y la etiqueta Courses en Swagger.
router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# POST /courses: recibe datos validados y responde con el curso creado (201).
@router.post(
    "",
    response_model=CourseResponse,
    status_code=201
)
def create_course_endpoint(
    # FastAPI interpreta CourseCreate como el cuerpo JSON de la petición.
    course: CourseCreate,
    # Depends obtiene y libera la sesión mediante get_session.
    session: Session = Depends(get_session)
):

    return create_course(
        course,
        session
    )


# GET /courses: devuelve todos los cursos como una lista.
@router.get(
    "",
    response_model=list[CourseResponse]
)
def list_courses_endpoint(
    # Depends obtiene y libera la sesión mediante get_session.
    session: Session = Depends(get_session)
):

    return list_courses(session)


# GET /courses/{course_id}: toma el ID de la URL y lo valida como entero.
@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course_endpoint(
    course_id: int,
    # Depends obtiene y libera la sesión mediante get_session.
    session: Session = Depends(get_session)
):

    return get_course(
        course_id,
        session
    )
