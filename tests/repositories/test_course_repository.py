from uuid import UUID

import pytest

from app.models.person import Person
from app.models.teacher import Teacher
from app.repositories.course_repository import CourseRepository


@pytest.mark.asyncio
async def test_course_repository_crud(session):
    repository = CourseRepository(session)

    # CREATE Teacher
    person = Person(name="Test Course Teacher")
    session.add(person)
    await session.commit()
    await session.refresh(person)

    teacher = Teacher(
        employee_number="T-002",
        person_id=person.id,
    )

    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)

    # CREATE Course
    course = await repository.create(
        code="CS-101",
        title="Computer Science",
        teacher_id=teacher.id,
    )

    assert course.id is not None
    assert course.code == "CS-101"
    assert course.title == "Computer Science"
    assert course.teacher_id == teacher.id

    # GET BY ID
    found_course = await repository.get_by_id(course.id)

    assert found_course is not None
    assert found_course.id == course.id

    # GET ALL
    courses = await repository.get_all()

    assert any(c.id == course.id for c in courses)

    # UPDATE
    updated_course = await repository.update(
        course,
        code="CS-102",
        title="Advanced Computer Science",
        teacher_id=teacher.id,
    )

    assert updated_course.code == "CS-102"
    assert updated_course.title == "Advanced Computer Science"

    # Проверяваме UPDATE в базата
    found_course = await repository.get_by_id(course.id)

    assert found_course is not None
    assert found_course.code == "CS-102"

    # DELETE
    await repository.delete(found_course)

    deleted_course = await repository.get_by_id(course.id)

    assert deleted_course is None