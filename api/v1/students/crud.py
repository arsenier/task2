from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.students.schemas import (
    StudentCreate,
    StudentSchema,
    StudentUpdate,
    StudentUpdatePartial,
)
from core.models import Student
from core.models.group import Group


async def get_students(session: AsyncSession) -> list[Student]:
    stmt = select(Student).order_by(Student.id)
    result: Result = await session.execute(stmt)
    students = result.scalars().all()
    return list(students)


async def get_student(session: AsyncSession, student_id: int) -> Student | None:
    return await session.get(Student, student_id)


async def create_student(
    session: AsyncSession,
    student_in: StudentCreate,
) -> Student | None:
    student = Student(**student_in.model_dump())
    stmt = select(Group).where(Group.id == student.group_id)
    group = await session.scalar(stmt)
    if group is None:
        return None
    session.add(student)
    await session.commit()
    return student


async def update_student(
    session: AsyncSession,
    student: Student,
    student_update: StudentUpdate | StudentUpdatePartial,
    partial: bool = False,
) -> Student:
    for name, value in student_update.model_dump(exclude_unset=partial).items():
        setattr(student, name, value)
    await session.commit()
    return student


async def update_student_s_group(
    session: AsyncSession, student: Student, group_new: Group
):
    setattr(student, "group_id", group_new.id)
    await session.commit()
    return student


async def delete_student(
    session: AsyncSession,
    student: Student,
) -> None:
    await session.delete(student)
    await session.commit()
