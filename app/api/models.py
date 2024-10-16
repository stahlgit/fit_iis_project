from typing import List

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.base import (
    Base,
    BaseModelMixin,
    CreateException,
    MissingRequiredFieldException,
)


class Conference(BaseModelMixin, Base):
    __tablename__ = "conferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    place: Mapped[str] = mapped_column(String, nullable=False)
    time_from = mapped_column(DateTime, nullable=False)
    time_to = mapped_column(DateTime, nullable=False)
    price = mapped_column(Float, nullable=False)
    capacity = mapped_column(Integer, nullable=False)

    rooms: Mapped[List["Room"]] = relationship("Room", back_populates="conference")

    lectures: Mapped[List["Lecture"]] = relationship(
        "Lecture", back_populates="conference"
    )

    reservation = Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="conference", cascade="all, delete, delete-orphan"
    )
    given_presentations = Mapped[List["GivenPresentation"]] = relationship(
        "GivenPresentation", back_populates="conference"
    )

    __table_args__ = (
        CheckConstraint("time_from < time_to", name="Correct_time_sequence"),
    )


class User(BaseModelMixin, Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    role = mapped_column(String, nullable=False)  ##TODO Enum ???
    ## TODO Add password

    lectures = Mapped[List["Lecture"]] = relationship(
        "Lecture", back_populates="lecturer"
    )

    votings = Mapped[List["Voting"]] = relationship("Voting", back_populates="user")
    questions = Mapped[List["Question"]] = relationship(
        "Question", back_populates="user"
    )
    reservations = Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="user", cascade="all, delete, delete-orphan"
    )
    given_presentations = Mapped[List["GivenPresentation"]] = relationship(
        "GivenPresentation", back_populates="user"
    )


class Room(BaseModelMixin, Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    capacity = mapped_column(Integer, nullable=False)
    conference_id = mapped_column(Integer, ForeignKey("conferences.id"), nullable=False)

    lectures: Mapped[List["Lecture"]] = relationship("Lecture", back_populates="room")

    conference = relationship("Conference", back_populates="rooms")


class Reservation(BaseModelMixin, Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number_of_tickets = mapped_column(Integer, nullable=False)
    status = mapped_column(String, nullable=False)
    paid = mapped_column(Boolean, nullable=False)

    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    conference_id = mapped_column(Integer, ForeignKey("conferences.id"), nullable=False)

    user = relationship("User", back_populates="reservations")
    conference = relationship("Conference", back_populates="reservations")


class Ticket(BaseModelMixin, Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conference_id = mapped_column(Integer, nullable=False)
    time_created = mapped_column(DateTime, nullable=False)
    ## HOW ABOUT ??? price = mapped_column(Float, nullable=False)

    reservation_id = mapped_column(
        Integer, ForeignKey("reservations.id"), nullable=False
    )

    reservation = relationship("Reservation", back_populates="tickets")


class Lecture(BaseModelMixin, Base):
    __tablename__ = "lectures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    time_from = mapped_column(DateTime, nullable=False)
    time_to = mapped_column(DateTime, nullable=False)
    tags = mapped_column(String, nullable=False)
    image = mapped_column(String, nullable=False)

    room_id = mapped_column(Integer, ForeignKey("rooms.id"), nullable=False)
    conference_id = mapped_column(Integer, ForeignKey("conferences.id"), nullable=False)
    lecturer_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    room = relationship("Room", back_populates="lectures")
    conference = relationship("Conference", back_populates="lectures")
    lecturer = relationship("User", back_populates="lectures")

    votings = Mapped[List["Voting"]] = relationship("Voting", back_populates="lecture")

    questions = Mapped[List["Question"]] = relationship(
        "Question", back_populates="lecture"
    )

    __table_args__ = (
        CheckConstraint("time_from < time_to", name="Correct_time_sequence"),
    )


class GivenPresentation(BaseModelMixin, Base):
    __tablename__ = "given_presentations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    """ user_id = mapped_column(Integer, nullable=False)
    lecture_id = mapped_column(Integer, nullable=False) """
    design = mapped_column(String, nullable=False)
    status = mapped_column(String, nullable=False)

    user = relationship("User", back_populates="given_presentations")
    conference = relationship("Conference", back_populates="given_presentations")


class Voting(BaseModelMixin, Base):
    __tablename__ = "voting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user = relationship("User", back_populates="votings")
    lecture = relationship("Lecture", back_populates="votings")


class Question(BaseModelMixin, Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship("User", back_populates="questions")
    lecture = relationship("Lecture", back_populates="questions")
