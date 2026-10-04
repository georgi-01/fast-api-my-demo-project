from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person


class PersonRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str) -> Person:
        person = Person(name=name)

        self.session.add(person)
        await self.session.commit()
        await self.session.refresh(person)

        return person

    async def get_by_id(self, person_id: UUID) -> Person | None:
        result = await self.session.execute(
            select(Person).where(Person.id == person_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Person]:
        result = await self.session.execute(
            select(Person)
        )

        return list(result.scalars().all())

    async def update(
        self,
        person: Person,
        name: str,
    ) -> Person:
        person.name = name

        await self.session.commit()
        await self.session.refresh(person)

        return person

    async def delete(self, person: Person) -> None:
        await self.session.delete(person)
        await self.session.commit()