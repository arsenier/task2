from core.models.base import Base
from sqlalchemy.orm import Mapped


class Group(Base):
    group_number: Mapped[str]
