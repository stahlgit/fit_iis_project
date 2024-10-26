import enum
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import TSTZRANGE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.base import (
    Base,
    BaseModelMixin,
    CreateException,
    MissingRequiredFieldException,
)


class UserRole(enum.Enum):
    ADMIN = "admin"
    REGISTERED = "registered"
    GUEST = "guest"


class Conference(BaseModelMixin, Base):
    __tablename__ = "conferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    place: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    time_interval: Mapped[Optional[TSTZRANGE]] = mapped_column(
        "time_interval", TSTZRANGE, nullable=False
    )
    # TIME TO // TIME FROM ?
    price: Mapped[Optional[Float]] = mapped_column(Float, nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    rooms: Mapped[List["Room"]] = relationship("Room", back_populates="conference")

    lectures: Mapped[List["Lecture"]] = relationship(
        "Lecture", back_populates="conference", cascade="all, delete, delete-orphan"
    )

    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="conference", cascade="all, delete, delete-orphan"
    )

    given_presentations: Mapped[List["GivenPresentation"]] = relationship(
        "GivenPresentation",
        back_populates="conference"
        ## track history ???
    )


class User(BaseModelMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.GUEST
    )
    # TODO password hashing

    lectures: Mapped[List["Lecture"]] = relationship(
        "Lecture",
        back_populates="lecturer"
        # no histoty to annonymize
    )

    votings: Mapped[List["Voting"]] = relationship("Voting", back_populates="user")

    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="user"
    )

    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="user", cascade="all, delete, delete-orphan"
    )
    given_presentations: Mapped[List["GivenPresentation"]] = relationship(
        "GivenPresentation", back_populates="user"
    )


class Room(BaseModelMixin, Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    conference_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conferences.id"), nullable=True
    )

    lectures: Mapped[List["Lecture"]] = relationship("Lecture", back_populates="room")

    conference: Mapped["Conference"] = relationship(
        "Conference", back_populates="rooms"
    )


class Reservation(BaseModelMixin, Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number_of_tickets: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=True)
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True  # HERE WAS FALSE
    )
    conference_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conferences.id"), nullable=False
    )

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="reservations"
    )  # NEW OPTIONAL USER
    conference: Mapped["Conference"] = relationship(
        "Conference", back_populates="reservations"
    )
    tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket", back_populates="reservation", cascade="all, delete, delete-orphan"
    )


class Ticket(BaseModelMixin, Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    ## HOW ABOUT ??? price = mapped_column(Float, nullable=False)

    reservation: Mapped["Reservation"] = relationship(
        "Reservation", back_populates="tickets"
    )
    reservation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False
    )


class Lecture(BaseModelMixin, Base):
    __tablename__ = "lectures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    time_interval: Mapped[TSTZRANGE] = mapped_column(TSTZRANGE, nullable=True)

    tags: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    conference_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conferences.id", ondelete="CASCADE"), nullable=False
    )
    lecturer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    room: Mapped["Room"] = relationship("Room", back_populates="lectures")
    conference: Mapped["Conference"] = relationship(
        "Conference", back_populates="lectures"
    )
    lecturer: Mapped["User"] = relationship("User", back_populates="lectures")

    votings: Mapped[List["Voting"]] = relationship("Voting", back_populates="lecture")

    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="lecture", cascade="all, delete, delete-orphan"
    )


class GivenPresentation(BaseModelMixin, Base):
    __tablename__ = "given_presentations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    conference_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conferences.id"), nullable=False
    )
    proposal: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="given_presentations")
    conference: Mapped["Conference"] = relationship(
        "Conference", back_populates="given_presentations"
    )


class Voting(BaseModelMixin, Base):
    __tablename__ = "voting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    lecture_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lectures.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="votings")
    lecture: Mapped["Lecture"] = relationship("Lecture", back_populates="votings")

    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_check"),
    )


class Question(BaseModelMixin, Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    lecture_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lectures.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="questions")
    lecture: Mapped["Lecture"] = relationship("Lecture", back_populates="questions")
