import pytest

from app.models.person import Person
from app.repositories.teacher_repository import TeacherRepository


@pytest.mark.asyncio
async def test_teacher_repository_crud(session):
    repository = TeacherRepository(session)

    # Създаваме Person, защото Teacher има FK към person.id
    person = Person(name="Test Teacher Person")

    session.add(person)
    await session.commit()
    await session.refresh(person)

    # CREATE
    teacher = await repository.create(
        employee_number="EMP-001",
        person_id=person.id,
    )

    assert teacher.id is not None
    assert teacher.employee_number == "EMP-001"
    assert teacher.person_id == person.id

    # GET BY ID
    found_teacher = await repository.get_by_id(teacher.id)

    assert found_teacher is not None
    assert found_teacher.id == teacher.id
    assert found_teacher.employee_number == "EMP-001"
    assert found_teacher.person_id == person.id

    # GET ALL
    teachers = await repository.get_all()

    assert any(t.id == teacher.id for t in teachers)

    # UPDATE
    updated_teacher = await repository.update(
        teacher,
        employee_number="EMP-002",
        person_id=person.id,
    )

    assert updated_teacher.id == teacher.id
    assert updated_teacher.employee_number == "EMP-002"
    assert updated_teacher.person_id == person.id

    # Проверяваме UPDATE в базата
    found_teacher = await repository.get_by_id(teacher.id)

    assert found_teacher is not None
    assert found_teacher.employee_number == "EMP-002"

    # DELETE
    await repository.delete(found_teacher)

    # Проверяваме DELETE
    deleted_teacher = await repository.get_by_id(teacher.id)

    assert deleted_teacher is None