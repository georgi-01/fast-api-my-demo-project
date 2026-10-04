from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        student_number: str,
        person_id: UUID,
    ) -> Student:
        student = Student(
            student_number=student_number,
            person_id=person_id,
        )

        self.session.add(student)

        await self.session.commit()
        await self.session.refresh(student)

        return student

    async def get_by_id(
        self,
        student_id: UUID,
    ) -> Student | None:
        result = await self.session.execute(
            select(Student).where(Student.id == student_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Student]:
        result = await self.session.execute(
            select(Student)
        )

        return list(result.scalars().all())

    async def update(
        self,
        student: Student,
        student_number: str,
        person_id: UUID,
    ) -> Student:
        student.student_number = student_number
        student.person_id = person_id

        await self.session.commit()
        await self.session.refresh(student)

        return student

    async def delete(self, student: Student) -> None:
        await self.session.delete(student)
        await self.session.commit()