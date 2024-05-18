from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Path, status

from api.v1.groups import crud
from core.models import db_helper
from core.models.group import Group


async def group_by_id(
    group_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Group:
    group = await crud.get_group_by_id(session=session, group_id=group_id)
    if group is not None:
        return group

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Group {group_id} not found!",
    )


async def group_by_number(
    group_number: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Group:
    group = await crud.get_group_by_number(session=session, group_number=group_number)
    if group is not None:
        return group

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Group {group_number} not found!",
    )
