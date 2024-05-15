from core.models.base import Base
from sqlalchemy.orm import Mapped


class Student(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    group_id: Mapped[int | None]
