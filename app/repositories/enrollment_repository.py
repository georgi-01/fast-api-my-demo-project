from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment


class EnrollmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        student_id: UUID,
        course_id: UUID,
        date_value: date,
    ) -> Enrollment:
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            date=date_value,
        )

        self.session.add(enrollment)
        await self.session.commit()
        await self.session.refresh(enrollment)

        return enrollment

    async def get_by_id(
        self,
        enrollment_id: UUID,
    ) -> Enrollment | None:
        result = await self.session.execute(
            select(Enrollment).where(
                Enrollment.id == enrollment_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Enrollment]:
        result = await self.session.execute(
            select(Enrollment)
        )

        return list(result.scalars().all())

    async def update(
        self,
        enrollment: Enrollment,
        student_id: UUID,
        course_id: UUID,
        date_value: date,
    ) -> Enrollment:
        enrollment.student_id = student_id
        enrollment.course_id = course_id
        enrollment.date = date_value

        await self.session.commit()
        await self.session.refresh(enrollment)

        return enrollment

    async def delete(self, enrollment: Enrollment) -> None:
        await self.session.delete(enrollment)
        await self.session.commit()