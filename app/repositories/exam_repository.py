from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exam import Exam


class ExamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        course_id: UUID,
        date_value: date,
        weight: float,
    ) -> Exam:
        exam = Exam(
            course_id=course_id,
            date=date_value,
            weight=weight,
        )

        self.session.add(exam)
        await self.session.commit()
        await self.session.refresh(exam)

        return exam

    async def get_by_id(self, exam_id: UUID) -> Exam | None:
        result = await self.session.execute(
            select(Exam).where(Exam.id == exam_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Exam]:
        result = await self.session.execute(
            select(Exam)
        )

        return list(result.scalars().all())

    async def update(
        self,
        exam: Exam,
        course_id: UUID,
        date_value: date,
        weight: float,
    ) -> Exam:
        exam.course_id = course_id
        exam.date = date_value
        exam.weight = weight

        await self.session.commit()
        await self.session.refresh(exam)

        return exam

    async def delete(self, exam: Exam) -> None:
        await self.session.delete(exam)
        await self.session.commit()