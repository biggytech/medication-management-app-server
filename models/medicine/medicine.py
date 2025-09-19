from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import Base

@dataclass
class Medicine(Base):
    __tablename__ = "medicine"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    def __repr__(self) -> str:
        return f"Medicine(id={self.id!r}, title={self.title!r})"
