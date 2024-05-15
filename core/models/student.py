from sqlalchemy import ForeignKey, String
from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Student(Base):
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"),
    )
