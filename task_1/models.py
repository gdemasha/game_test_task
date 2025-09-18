from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

from task_1.config import Base, settings


class Player(Base):
    """User details table"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    # time of first login:
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc)
    )
    # points for everyday login:
    daily_points: Mapped[int] = mapped_column(default=0)
    # some general user info:
    name: Mapped[str] = mapped_column(default='User')
    phone_number: Mapped[str] = mapped_column(default=None, nullable=True)
    # we can also keep a list of available boosts:
    boosts: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String)),
        nullable=True,
        default=[]
    )


class Boost(Base):
    """Boosts table"""

    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(default='Boost')
    description: Mapped[str] = mapped_column(default=None, nullable=True)


class UserBoosts(Base):
    """User's boosts table."""

    __tablename__ = 'user_boots'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    boost_id: Mapped[int] = mapped_column(
        ForeignKey('boosts.id', ondelete='SET NULL')
    )
    count: Mapped[int] = mapped_column(default=0)


Base.metadata.create_all(settings.alchemy_engine)
