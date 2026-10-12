
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from .base import Base
import datetime



class AppsTime(Base):

    __tablename__ = "appstime"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column()
    app: Mapped[str] = mapped_column()
    seconds: Mapped[int] = mapped_column()
    __table_args__ = (UniqueConstraint(date, app, name="uq_appstime_date_app"),)
