import asyncio

from sqlalchemy import select

from datetime import date

from app.database.database import SessionLocal
from app.models.person import Person
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.exam import Exam


async def seed_people() -> bool:
    seeded = False

    async with SessionLocal() as session:
        # =========================
        # TEACHERS
        # =========================

        teachers_data = [
            {
                "name": "Ivan Petrov",
                "employee_number": "T-001",
            },
            {
                "name": "Maria Ivanova",
                "employee_number": "T-002",
            },
            {
                "name": "Georgi Dimitrov",
                "employee_number": "T-003",
            },
        ]

        for data in teachers_data:
            result = await session.execute(
                select(Teacher).where(
                    Teacher.employee_number == data["employee_number"]
                )
            )

            teacher = result.scalar_one_or_none()

            if teacher is not None:
                continue

            person = Person(name=data["name"])
            session.add(person)

            await session.flush()

            teacher = Teacher(
                employee_number=data["employee_number"],
                person_id=person.id,
            )

            session.add(teacher)
            seeded = True

        # =========================
        # STUDENTS
        # =========================

        students_data = [
            {
                "name": "Anna Georgieva",
                "student_number": "ST-001",
            },
            {
                "name": "Petar Nikolov",
                "student_number": "ST-002",
            },
            {
                "name": "Elena Todorova",
                "student_number": "ST-003",
            },
            {
                "name": "Nikolay Stoyanov",
                "student_number": "ST-004",
            },
            {
                "name": "Viktoria Petrova",
                "student_number": "ST-005",
            },
        ]

        for data in students_data:
            result = await session.execute(
                select(Student).where(
                    Student.student_number == data["student_number"]
                )
            )

            student = result.scalar_one_or_none()

            if student is not None:
                continue

            person = Person(name=data["name"])
            session.add(person)

            await session.flush()

            student = Student(
                student_number=data["student_number"],
                person_id=person.id,
            )

            session.add(student)
            seeded = True

        # =========================
        # COURSES
        # =========================

        courses_data = [
            {
                "code": "CS101",
                "title": "Introduction to Programming",
                "employee_number": "T-001",
            },
            {
                "code": "CS102",
                "title": "Database Systems",
                "employee_number": "T-002",
            },
            {
                "code": "CS103",
                "title": "Web Development",
                "employee_number": "T-003",
            },
        ]

        for data in courses_data:
            result = await session.execute(
                select(Teacher).where(
                    Teacher.employee_number == data["employee_number"]
                )
            )

            teacher = result.scalar_one()

            result = await session.execute(
                select(Course).where(
                    Course.code == data["code"]
                )
            )

            course = result.scalar_one_or_none()

            if course is not None:
                continue

            course = Course(
                code=data["code"],
                title=data["title"],
                teacher_id=teacher.id,
            )

            session.add(course)
            seeded = True

        # =========================
        # ENROLLMENTS
        # =========================

        enrollments_data = [
            {
                "student_number": "ST-001",
                "course_code": "CS101",
                "date": date(2026, 9, 15),
            },
            {
                "student_number": "ST-001",
                "course_code": "CS102",
                "date": date(2026, 9, 15),
            },
            {
                "student_number": "ST-002",
                "course_code": "CS101",
                "date": date(2026, 9, 16),
            },
            {
                "student_number": "ST-002",
                "course_code": "CS103",
                "date": date(2026, 9, 16),
            },
            {
                "student_number": "ST-003",
                "course_code": "CS102",
                "date": date(2026, 9, 17),
            },
            {
                "student_number": "ST-004",
                "course_code": "CS101",
                "date": date(2026, 9, 18),
            },
            {
                "student_number": "ST-005",
                "course_code": "CS103",
                "date": date(2026, 9, 18),
            },
        ]

        for data in enrollments_data:
            result = await session.execute(
                select(Student).where(
                    Student.student_number == data["student_number"]
                )
            )
            student = result.scalar_one()

            result = await session.execute(
                select(Course).where(
                    Course.code == data["course_code"]
                )
            )
            course = result.scalar_one()

            result = await session.execute(
                select(Enrollment).where(
                    Enrollment.student_id == student.id,
                    Enrollment.course_id == course.id,
                )
            )
            enrollment = result.scalar_one_or_none()

            if enrollment is not None:
                continue

            enrollment = Enrollment(
                student_id=student.id,
                course_id=course.id,
                date=data["date"],
            )

            session.add(enrollment)
            seeded = True

        # =========================
        # EXAMS
        # =========================

        exams_data = [
            {
                "course_code": "CS101",
                "date": date(2026, 10, 20),
                "weight": 0.40,
            },
            {
                "course_code": "CS102",
                "date": date(2026, 10, 22),
                "weight": 0.50,
            },
            {
                "course_code": "CS103",
                "date": date(2026, 10, 24),
                "weight": 0.60,
            },
        ]

        for data in exams_data:
            result = await session.execute(
                select(Course).where(
                    Course.code == data["course_code"]
                )
            )
            course = result.scalar_one()

            result = await session.execute(
                select(Exam).where(
                    Exam.course_id == course.id,
                    Exam.date == data["date"],
                )
            )
            exam = result.scalar_one_or_none()

            if exam is not None:
                continue

            exam = Exam(
                course_id=course.id,
                date=data["date"],
                weight=data["weight"],
            )

            session.add(exam)
            seeded = True

        await session.commit()

    return seeded

async def main() -> None:
    seeded = await seed_people()

    if seeded:
        print("Database seeding completed.")
    else:
        print("Database already seeded.")


if __name__ == "__main__":
    asyncio.run(main())