import pytest

from app.repositories.person_repository import PersonRepository


@pytest.mark.asyncio
async def test_person_repository_crud(session):
    repository = PersonRepository(session)

    # CREATE
    person = await repository.create("Test Person")

    assert person.id is not None
    assert person.name == "Test Person"

    # GET BY ID
    found_person = await repository.get_by_id(person.id)

    assert found_person is not None
    assert found_person.id == person.id
    assert found_person.name == "Test Person"

    # GET ALL
    people = await repository.get_all()

    assert any(p.id == person.id for p in people)

    # UPDATE
    updated_person = await repository.update(
        person,
        "Updated Test Person",
    )

    assert updated_person.id == person.id
    assert updated_person.name == "Updated Test Person"

    # Проверяваме UPDATE в базата
    found_person = await repository.get_by_id(person.id)

    assert found_person is not None
    assert found_person.name == "Updated Test Person"

    # DELETE
    await repository.delete(found_person)

    # Проверяваме DELETE
    deleted_person = await repository.get_by_id(person.id)

    assert deleted_person is None