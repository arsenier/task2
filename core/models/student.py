from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from group import Group


class Student(Base):
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"),
    )
    group: Mapped["Group"] = relationship(back_populates="students")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.first_name} {self.last_name}, group: {self.group_id})"

    def __repr__(self):
        return str(self)
