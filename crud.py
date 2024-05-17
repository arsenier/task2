import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.students.schemas import StudentCreate
from core.models import db_helper
from core.models.group import Group
from core.models.student import Student


async def create_group(session: AsyncSession, group_number: str) -> Group:
    group = Group(group_number=group_number)
    session.add(group)
    await session.commit()
    print("group", group)  # TODO remove in prod
    return group


async def get_groups(session: AsyncSession) -> list[Group]:
    stmt = select(Group).order_by(Group.id)
    groups = await session.scalars(stmt)

    for group in groups:  # TODO remove in prod
        print("group", group)
    return groups


async def get_group_by_id(session: AsyncSession, group_id: int) -> Group:
    stmt = select(Group).where(Group.id == group_id)
    group = await session.scalar(stmt)
    # print(group)
    return group


async def get_group_by_number(session: AsyncSession, group_number: str) -> Group:
    stmt = select(Group).where(Group.group_number == group_number)
    group = await session.scalar(stmt)
    print(group)
    return group


async def delete_group(session: AsyncSession, group: Group) -> None:
    stmt = select(Student).where(Student.group_id == group.id).order_by(Student.id)
    student_in_group = await session.scalars(stmt)

    for student in student_in_group:
        await delete_student(session, student)

    await session.delete(group)
    await session.commit()


async def create_student(
    session: AsyncSession,
    student_in: StudentCreate,
) -> Student:
    student = Student(**student_in.model_dump())
    session.add(student)
    await session.commit()
    print(student)
    return student


async def get_students(session: AsyncSession) -> list[Student]:
    stmt = select(Student).order_by(Student.id)
    students = await session.scalars(stmt)

    for student in students:  # TODO remove in prod
        print("student", student)
    return students


async def get_student_by_id(session: AsyncSession, student_id: int) -> Student:
    stmt = select(Student).where(Student.id == student_id)
    student = await session.scalar(stmt)
    print(student)
    return student


async def delete_student(
    session: AsyncSession,
    student: Student,
) -> None:
    await session.delete(student)
    await session.commit()


async def get_students_in_group(session: AsyncSession, group: Group) -> list[Student]:
    stmt = (
        select(Group).options(selectinload(Group.students)).where(Group.id == group.id)
    )
    group = await session.scalar(stmt)
    students = group.students
    print(group)
    for student in students:
        print(student)
    return students


async def update_student_s_group(
    session: AsyncSession, student: Student, group_new: Group
):
    setattr(student, "group_id", group_new.id)
    await session.commit()
    print(student)
    return student


async def main():
    async with db_helper.session_factory() as session:
        # await create_group(session=session, group_number="3532704/90201")
        # await create_group(session=session, group_number="5142704/30801")
        # await create_group(session=session, group_number="OLOOLOLOLLO")
        # await delete_group(session, await get_group_by_id(session, 4))

        # student_in = StudentCreate(first_name="Boris", last_name="Borisov", group_id=2)
        # student_in = StudentCreate(
        #     first_name="Nikolay", last_name="Kolovski", group_id=2
        # )
        # student_in = StudentCreate(first_name="Nikita", last_name="Faller", group_id=2)
        # student_in = StudentCreate(first_name="Leonid", last_name="Ilyich", group_id=3)
        # await create_student(session=session, student_in=student_in)

        # await get_groups(session)
        # await get_group_by_id(session, 1)
        # await get_student_by_id(session, 2)
        # await delete_student(session, await get_student_by_id(session, 3))
        # await get_students_in_group(
        #     session,
        #     await get_group_by_id(session, 2),
        # )

        # student = await get_student_by_id(session, 6)
        # group_new = await get_group_by_id(session, 2)
        # await update_student_s_group(session, student, group_new)
        # await get_students_in_group(
        #     session,
        #     await get_group_by_id(session, 2),
        # )

        # await get_group_by_number(session, "5142704/30801")

        # await get_students(session)

        pass


if __name__ == "__main__":
    asyncio.run(main())
