from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001"
down_revision: str | None = None


def upgrade() -> None:
    op.create_table(
        "person",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "name",
            sa.String(255),
            nullable=False,
        ),
    )

    op.create_table(
        "student",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "student_number",
            sa.String(50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "person_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("person.id"),
            nullable=False,
            unique=True,
        ),
    )

    op.create_table(
        "teacher",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "employee_number",
            sa.String(50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "person_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("person.id"),
            nullable=False,
            unique=True,
        ),
    )

    op.create_table(
        "course",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "code",
            sa.String(50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "title",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "teacher_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("teacher.id"),
            nullable=False,
        ),
    )

    op.create_table(
        "enrollment",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "student_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("student.id"),
            nullable=False,
        ),
        sa.Column(
            "course_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("course.id"),
            nullable=False,
        ),
        sa.Column(
            "date",
            sa.Date(),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "student_id",
            "course_id",
            name="uq_enrollment_student_course",
        ),
    )

    op.create_table(
        "exam",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "course_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "course.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "date",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "weight",
            sa.Float(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("exam")
    op.drop_table("enrollment")
    op.drop_table("course")
    op.drop_table("teacher")
    op.drop_table("student")
    op.drop_table("person")