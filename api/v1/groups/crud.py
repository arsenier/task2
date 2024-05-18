from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.groups.schemas import GroupCreate
import api.v1.students.crud as student_crud
from core.models.group import Group
from core.models.student import Student


async def create_group(
    session: AsyncSession,
    group_in: GroupCreate,
) -> Group:
    group = Group(**group_in.model_dump())
    session.add(group)
    await session.commit()
    return group


# async def create_group(session: AsyncSession, group_number: str) -> Group:
#     group = Group(group_number=group_number)
#     session.add(group)
#     await session.commit()
#     return group


async def get_groups(session: AsyncSession) -> list[Group]:
    stmt = select(Group).order_by(Group.id)
    groups = await session.scalars(stmt)
    return groups


async def get_group_by_id(session: AsyncSession, group_id: int) -> Group:
    stmt = select(Group).where(Group.id == group_id)
    group = await session.scalar(stmt)
    return group


async def get_group_by_number(session: AsyncSession, group_number: str) -> Group:
    stmt = select(Group).where(Group.group_number == group_number)
    group = await session.scalar(stmt)
    return group


async def delete_group(session: AsyncSession, group: Group) -> None:
    stmt = select(Student).where(Student.group_id == group.id).order_by(Student.id)
    student_in_group = await session.scalars(stmt)

    for student in student_in_group:
        await student_crud.delete_student(session, student)

    await session.delete(group)
    await session.commit()


async def get_students_in_group(session: AsyncSession, group: Group) -> list[Student]:
    stmt = (
        select(Group).options(selectinload(Group.students)).where(Group.id == group.id)
    )
    group = await session.scalar(stmt)
    students = group.students
    return students
