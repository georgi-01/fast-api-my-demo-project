from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teacher import Teacher


class TeacherRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        employee_number: str,
        person_id,
    ) -> Teacher:
        teacher = Teacher(
            employee_number=employee_number,
            person_id=person_id,
        )

        self.session.add(teacher)
        await self.session.commit()
        await self.session.refresh(teacher)

        return teacher

    async def get_by_id(self, teacher_id) -> Teacher | None:
        result = await self.session.execute(
            select(Teacher).where(Teacher.id == teacher_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Teacher]:
        result = await self.session.execute(
            select(Teacher)
        )

        return list(result.scalars().all())

    async def update(
        self,
        teacher: Teacher,
        **fields,
    ) -> Teacher:
        for field, value in fields.items():
            setattr(teacher, field, value)

        await self.session.commit()
        await self.session.refresh(teacher)

        return teacher

    async def delete(self, teacher: Teacher) -> None:
        await self.session.delete(teacher)
        await self.session.commit()