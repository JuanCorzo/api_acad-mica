# Los servicios realizan las operaciones de datos que solicitan los routers.
from fastapi import HTTPException
from sqlmodel import Session, select

from models.course import Course
from schemas.course import CourseCreate, CourseUpdate


def create_course(
    course_data: CourseCreate,
    session: Session
):

    # Convierte los datos de entrada en una entidad que puede persistirse.
    course = Course(
        name=course_data.name,
        credits=course_data.credits,
        active=course_data.active
    )

    # Registra el objeto en la sesión, todavía sin confirmar la transacción.
    session.add(course)
    # Confirma la inserción en la base de datos.
    session.commit()
    # Recarga los valores guardados, como el ID generado por SQLite.
    session.refresh(course)

    return course


def list_courses(session: Session):

    # Construye una consulta para recuperar todos los registros de Course.
    statement = select(Course)

    # Ejecuta la consulta y reúne los resultados en una lista.
    courses = session.exec(statement).all()

    return courses


def get_course(
    course_id: int,
    session: Session
):

    # Busca por clave primaria; devuelve None si no existe ese ID.
    course = session.get(
        Course,
        course_id
    )

    # Informa al cliente de un recurso inexistente con el estado HTTP 404.
    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


def update_course(
    course_id: int,
    course_data: CourseUpdate,
    session: Session
):

    # Busca el curso existente; reutiliza el 404 si no está.
    course = get_course(course_id, session)

    # Actualiza sobre el mismo objeto para conservar el ID.
    course.name = course_data.name
    course.credits = course_data.credits
    course.active = course_data.active

    session.add(course)
    session.commit()
    session.refresh(course)

    return course


def delete_course(
    course_id: int,
    session: Session
):

    # Reutiliza la búsqueda y el 404 si el curso no existe.
    course = get_course(course_id, session)

    # Marca el registro para eliminación y confirma en SQLite.
    session.delete(course)
    session.commit()

    return {"message": "Course deleted"}
