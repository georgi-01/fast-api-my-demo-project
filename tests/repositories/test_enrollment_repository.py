from datetime import date

import pytest

from app.models.course import Course
from app.models.person import Person
from app.models.student import Student
from app.models.teacher import Teacher
from app.repositories.enrollment_repository import EnrollmentRepository


@pytest.mark.asyncio
async def test_enrollment_repository_crud(session):
    repository = EnrollmentRepository(session)

    # CREATE Person for Student
    student_person = Person(name="Test Enrollment Student")
    session.add(student_person)
    await session.commit()
    await session.refresh(student_person)

    # CREATE Student
    student = Student(
        student_number="ST-106",
        person_id=student_person.id,
    )

    session.add(student)
    await session.commit()
    await session.refresh(student)

    # CREATE Person for Teacher
    teacher_person = Person(name="Test Enrollment Teacher")
    session.add(teacher_person)
    await session.commit()
    await session.refresh(teacher_person)

    # CREATE Teacher
    teacher = Teacher(
        employee_number="T-101",
        person_id=teacher_person.id,
    )

    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)

    # CREATE Course
    course = Course(
        code="EN-101",
        title="Enrollment Course",
        teacher_id=teacher.id,
    )

    session.add(course)
    await session.commit()
    await session.refresh(course)

    # CREATE Enrollment
    enrollment = await repository.create(
        student_id=student.id,
        course_id=course.id,
        date_value=date(2026, 10, 5),
    )

    assert enrollment.id is not None
    assert enrollment.student_id == student.id
    assert enrollment.course_id == course.id
    assert enrollment.date == date(2026, 10, 5)

    # GET BY ID
    found_enrollment = await repository.get_by_id(enrollment.id)

    assert found_enrollment is not None
    assert found_enrollment.id == enrollment.id

    # GET ALL
    enrollments = await repository.get_all()

    assert any(e.id == enrollment.id for e in enrollments)

    # UPDATE
    updated_enrollment = await repository.update(
        enrollment,
        student_id=student.id,
        course_id=course.id,
        date_value=date(2026, 10, 6),
    )

    assert updated_enrollment.date == date(2026, 10, 6)

    # Проверяваме UPDATE в базата
    found_enrollment = await repository.get_by_id(enrollment.id)

    assert found_enrollment is not None
    assert found_enrollment.date == date(2026, 10, 6)

    # DELETE
    await repository.delete(found_enrollment)

    deleted_enrollment = await repository.get_by_id(enrollment.id)

    assert deleted_enrollment is None