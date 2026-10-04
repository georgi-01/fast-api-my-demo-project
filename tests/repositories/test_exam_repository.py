from datetime import date

import pytest

from app.models.course import Course
from app.models.person import Person
from app.models.teacher import Teacher
from app.repositories.exam_repository import ExamRepository


@pytest.mark.asyncio
async def test_exam_repository_crud(session):
    repository = ExamRepository(session)

    # CREATE Person for Teacher
    person = Person(name="Test Exam Teacher")
    session.add(person)
    await session.commit()
    await session.refresh(person)

    # CREATE Teacher
    teacher = Teacher(
        employee_number="T-202",
        person_id=person.id,
    )

    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)

    # CREATE Course
    course = Course(
        code="EX-202",
        title="Exam Course",
        teacher_id=teacher.id,
    )

    session.add(course)
    await session.commit()
    await session.refresh(course)

    # CREATE Exam
    exam = await repository.create(
        course_id=course.id,
        date_value=date(2026, 10, 10),
        weight=30.0,
    )

    assert exam.id is not None
    assert exam.course_id == course.id
    assert exam.date == date(2026, 10, 10)
    assert exam.weight == 30.0

    # GET BY ID
    found_exam = await repository.get_by_id(exam.id)

    assert found_exam is not None
    assert found_exam.id == exam.id

    # GET ALL
    exams = await repository.get_all()

    assert any(e.id == exam.id for e in exams)

    # UPDATE
    updated_exam = await repository.update(
        exam,
        course_id=course.id,
        date_value=date(2026, 10, 15),
        weight=40.0,
    )

    assert updated_exam.date == date(2026, 10, 15)
    assert updated_exam.weight == 40.0

    # Проверяваме UPDATE в базата
    found_exam = await repository.get_by_id(exam.id)

    assert found_exam is not None
    assert found_exam.weight == 40.0

    # DELETE
    await repository.delete(found_exam)

    deleted_exam = await repository.get_by_id(exam.id)

    assert deleted_exam is None