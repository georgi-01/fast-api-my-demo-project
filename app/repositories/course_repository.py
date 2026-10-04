from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course


class CourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        code: str,
        title: str,
        teacher_id: UUID,
    ) -> Course:
        course = Course(
            code=code,
            title=title,
            teacher_id=teacher_id,
        )

        self.session.add(course)
        await self.session.commit()
        await self.session.refresh(course)

        return course

    async def get_by_id(self, course_id: UUID) -> Course | None:
        result = await self.session.execute(
            select(Course).where(Course.id == course_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Course]:
        result = await self.session.execute(
            select(Course)
        )

        return list(result.scalars().all())

    async def update(
        self,
        course: Course,
        code: str,
        title: str,
        teacher_id: UUID,
    ) -> Course:
        course.code = code
        course.title = title
        course.teacher_id = teacher_id

        await self.session.commit()
        await self.session.refresh(course)

        return course

    async def delete(self, course: Course) -> None:
        await self.session.delete(course)
        await self.session.commit()