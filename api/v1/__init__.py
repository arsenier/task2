from fastapi import APIRouter

from api.v1.students.views import router as students_router

router = APIRouter()
router.include_router(router=students_router, prefix="/students")
