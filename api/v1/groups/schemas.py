from pydantic import BaseModel

from api.v1.students.schemas import StudentSchema
from core.models.student import Student


class GroupBase(BaseModel):
    group_number: str


class GroupSchema(GroupBase):
    id: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupCreate):
    pass


class GroupUpdatePartial(GroupCreate):
    group_number: str | None


class GroupWithStudentsSchema(GroupSchema):
    students: list[StudentSchema]
