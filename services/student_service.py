from fastapi import HTTPException
from sqlmodel import Session, select

from models.student import Student
from schemas.student import StudentCreate


def create_student(student_data: StudentCreate, session: Session):
    student = Student(
        name=student_data.name,
        email=student_data.email,
        semester=student_data.semester,
        active=student_data.active
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def list_students(session: Session):
    statement = select(Student)
    students = session.exec(statement).all()
    return students


def get_student(student_id: int, session: Session):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
