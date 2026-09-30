
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import datetime

Base = declarative_base()


class AppSpendTime(Base):

    __tablename__ = "appstime"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column()
    app: Mapped[str] = mapped_column()
    seconds: Mapped[int] = mapped_column()