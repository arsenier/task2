from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Path, status

from api.v1.students import crud
from core.models import db_helper
from core.models.student import StudentModel


async def student_by_id(
    student_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> StudentModel:
    student = await crud.get_student(session=session, student_id=student_id)
    if student is not None:
        return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student {student_id} not found!",
    )
