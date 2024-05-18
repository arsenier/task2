from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.students.schemas import StudentSchema
from core.models.group import Group

from . import crud
from .schemas import GroupCreate, GroupSchema, GroupWithStudentsSchema
from core.models import db_helper

from .dependencies import group_by_id, group_by_number


router = APIRouter(tags=["Groups"])


@router.get("/", response_model=list[GroupSchema])
async def get_groups(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_groups(session=session)


@router.post("/", response_model=GroupSchema, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_in: GroupCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_group(session=session, group_in=group_in)


@router.get(
    "/{group_id}/",
    response_model=GroupSchema | GroupWithStudentsSchema,
)
async def get_group(
    group: Group = Depends(group_by_id),
    list_students: bool = False,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if not list_students:
        return group
    students_models = await crud.get_students_in_group(session=session, group=group)
    students = []
    for model in students_models:
        students.append(
            StudentSchema(
                first_name=model.first_name,
                last_name=model.last_name,
                group_id=model.group_id,
                id=model.id,
            )
        )
    group_with_students = GroupWithStudentsSchema(
        id=group.id,
        group_number=group.group_number,
        students=students,
    )
    return group_with_students


@router.delete(
    "/{group_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
    group: Group = Depends(group_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_group(
        session=session,
        group=group,
    )
