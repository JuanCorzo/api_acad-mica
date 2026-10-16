from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_session
from schemas.course import CourseCreate, CourseUpdate, CourseResponse
from services.course_service import (
    create_course,
    list_courses,
    get_course,
    update_course,
    delete_course
)

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("", response_model=CourseResponse, status_code=201)
def create_course_endpoint(
    course: CourseCreate,
    session: Session = Depends(get_session)
):
    return create_course(course, session)


@router.get("", response_model=list[CourseResponse])
def list_courses_endpoint(session: Session = Depends(get_session)):
    return list_courses(session)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course_endpoint(
    course_id: int,
    session: Session = Depends(get_session)
):
    return get_course(course_id, session)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course_endpoint(
    course_id: int,
    course: CourseUpdate,
    session: Session = Depends(get_session)
):
    return update_course(course_id, course, session)


@router.delete("/{course_id}", status_code=200)
def delete_course_endpoint(
    course_id: int,
    session: Session = Depends(get_session)
):
    return delete_course(course_id, session)
