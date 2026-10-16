# Los servicios realizan las operaciones de datos que solicitan los routers.
from fastapi import HTTPException
from sqlmodel import Session, select

from models.student import Student
from schemas.student import StudentCreate


def create_student(
    student_data: StudentCreate,
    session: Session
):

    # Convierte los datos de entrada en una entidad que puede persistirse.
    student = Student(
        name=student_data.name,
        email=student_data.email,
        semester=student_data.semester,
        active=student_data.active
    )

    # Registra el objeto en la sesión, todavía sin confirmar la transacción.
    session.add(student)
    # Confirma la inserción en la base de datos.
    session.commit()
    # Recarga los valores guardados, como el ID generado por SQLite.
    session.refresh(student)

    return student


def list_students(session: Session):

    # Construye una consulta para recuperar todos los registros de Student.
    statement = select(Student)

    # Ejecuta la consulta y reúne los resultados en una lista.
    students = session.exec(statement).all()

    return students


def get_student(
    student_id: int,
    session: Session
):

    # Busca por clave primaria; devuelve None si no existe ese ID.
    student = session.get(
        Student,
        student_id
    )

    # Informa al cliente de un recurso inexistente con el estado HTTP 404.
    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student
