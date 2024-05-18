from typing import TYPE_CHECKING

from sqlalchemy import String
from core.models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from student import Student


class Group(Base):
    group_number: Mapped[str] = mapped_column(String(20), unique=True)
    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, group={self.group_number})"

    def __repr__(self):
        return str(self)
