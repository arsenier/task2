from pydantic import BaseModel


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    group_id: int


class StudentSchema(StudentBase):
    id: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentCreate):
    pass


class StudentUpdatePartial(StudentCreate):
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = None
