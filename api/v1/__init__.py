from fastapi import APIRouter

from api.v1.students.views import router as students_router
from api.v1.groups.views import router as groups_router

router = APIRouter()
router.include_router(router=students_router, prefix="/students")
router.include_router(router=groups_router, prefix="/groups")
