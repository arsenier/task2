from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.groups.dependencies import group_by_id
from api.v1.students import crud
from api.v1.students.dependencies import student_by_id
from api.v1.students.schemas import (
    StudentCreate,
    StudentSchema,
    StudentUpdate,
    StudentUpdatePartial,
)
from core.models import db_helper
from core.models.group import Group
from core.models.student import Student


router = APIRouter(tags=["Students"])


@router.get("/", response_model=list[StudentSchema])
async def get_students(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_students(session=session)


@router.post(
    "/",
    response_model=StudentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    student_in: StudentCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    student = await crud.create_student(student_in=student_in, session=session)
    if student is not None:
        return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Group {student_in.group_id} does not exist!",
    )


@router.get(
    "/{student_id}/",
    response_model=StudentSchema,
)
async def get_student(
    student: StudentSchema = Depends(student_by_id),
):
    return student


@router.put("/{student_id}/")
async def update_student(
    student_update: StudentUpdate,
    student: StudentSchema = Depends(student_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_student(
        session=session,
        student=student,
        student_update=student_update,
    )


# @router.patch("/{student_id}/")
# async def update_student_partial(
#     student_update: StudentUpdatePartial,
#     student: StudentSchema = Depends(student_by_id),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.update_student(
#         session=session,
#         student=student,
#         student_update=student_update,
#         partial=True,
#     )


@router.patch("/{student_id}/")
async def update_student_s_group(
    student: Student = Depends(student_by_id),
    group_new: Group = Depends(group_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_student_s_group(
        session=session,
        student=student,
        group_new=group_new,
    )


@router.delete("/{student_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student: StudentSchema = Depends(student_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_student(
        session=session,
        student=student,
    )
