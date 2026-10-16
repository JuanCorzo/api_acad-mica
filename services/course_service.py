from fastapi import HTTPException
from sqlmodel import Session, select

from models.course import Course
from schemas.course import CourseCreate, CourseUpdate


def create_course(course_data: CourseCreate, session: Session):
    course = Course(
        name=course_data.name,
        credits=course_data.credits,
        active=course_data.active
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def list_courses(session: Session):
    statement = select(Course)
    courses = session.exec(statement).all()
    return courses


def get_course(course_id: int, session: Session):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def update_course(course_id: int, course_data: CourseUpdate, session: Session):
    course = get_course(course_id, session)
    course.name = course_data.name
    course.credits = course_data.credits
    course.active = course_data.active
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def delete_course(course_id: int, session: Session):
    course = get_course(course_id, session)
    session.delete(course)
    session.commit()
    return {"message": "Course deleted"}
