import pytest

from app.models.person import Person
from app.repositories.student_repository import StudentRepository


@pytest.mark.asyncio
async def test_student_repository_crud(session):
    repository = StudentRepository(session)

    # Създаваме Person, защото Student има FK към person.id
    person = Person(name="Test Student Person")

    session.add(person)
    await session.commit()
    await session.refresh(person)

    # CREATE
    student = await repository.create(
        student_number="ST-001",
        person_id=person.id,
    )

    assert student.id is not None
    assert student.student_number == "ST-001"
    assert student.person_id == person.id

    # GET BY ID
    found_student = await repository.get_by_id(student.id)

    assert found_student is not None
    assert found_student.id == student.id
    assert found_student.student_number == "ST-001"
    assert found_student.person_id == person.id

    # GET ALL
    students = await repository.get_all()

    assert any(s.id == student.id for s in students)

    # UPDATE
    updated_student = await repository.update(
        student,
        student_number="ST-002",
        person_id=person.id,
    )

    assert updated_student.id == student.id
    assert updated_student.student_number == "ST-002"
    assert updated_student.person_id == person.id

    # Проверяваме UPDATE в базата
    found_student = await repository.get_by_id(student.id)

    assert found_student is not None
    assert found_student.student_number == "ST-002"

    # DELETE
    await repository.delete(found_student)

    # Проверяваме DELETE
    deleted_student = await repository.get_by_id(student.id)

    assert deleted_student is None