"""Organizer

Revision ID: d748d28f5208
Revises: a0fb280cf237
Create Date: 2024-11-23 16:02:32.960763

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d748d28f5208"
down_revision: Union[str, None] = "a0fb280cf237"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("conferences", sa.Column("organizer_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None,
        "conferences",
        "users",
        ["organizer_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.drop_constraint(
        "given_presentations_user_id_fkey", "given_presentations", type_="foreignkey"
    )
    op.drop_constraint(
        "given_presentations_conference_id_fkey",
        "given_presentations",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "given_presentations",
        "conferences",
        ["conference_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.create_foreign_key(
        None,
        "given_presentations",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.drop_constraint("lectures_conference_id_fkey", "lectures", type_="foreignkey")
    op.drop_constraint("lectures_room_id_fkey", "lectures", type_="foreignkey")
    op.drop_constraint("lectures_lecturer_id_fkey", "lectures", type_="foreignkey")
    op.create_foreign_key(
        None,
        "lectures",
        "rooms",
        ["room_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "lectures",
        "conferences",
        ["conference_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "lectures",
        "users",
        ["lecturer_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
        ondelete="CASCADE",
    )
    op.drop_constraint("questions_lecture_id_fkey", "questions", type_="foreignkey")
    op.drop_constraint("questions_user_id_fkey", "questions", type_="foreignkey")
    op.create_foreign_key(
        None,
        "questions",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.create_foreign_key(
        None,
        "questions",
        "lectures",
        ["lecture_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.drop_constraint(
        "reservations_conference_id_fkey", "reservations", type_="foreignkey"
    )
    op.drop_constraint("reservations_user_id_fkey", "reservations", type_="foreignkey")
    op.create_foreign_key(
        None,
        "reservations",
        "conferences",
        ["conference_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.create_foreign_key(
        None,
        "reservations",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.drop_constraint("rooms_conference_id_fkey", "rooms", type_="foreignkey")
    op.create_foreign_key(
        None,
        "rooms",
        "conferences",
        ["conference_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.drop_constraint("tickets_reservation_id_fkey", "tickets", type_="foreignkey")
    op.create_foreign_key(
        None,
        "tickets",
        "reservations",
        ["reservation_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
        ondelete="CASCADE",
    )
    op.drop_constraint("voting_user_id_fkey", "voting", type_="foreignkey")
    op.drop_constraint("voting_lecture_id_fkey", "voting", type_="foreignkey")
    op.create_foreign_key(
        None,
        "voting",
        "lectures",
        ["lecture_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.create_foreign_key(
        None,
        "voting",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "voting", schema="public", type_="foreignkey")
    op.drop_constraint(None, "voting", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "voting_lecture_id_fkey", "voting", "lectures", ["lecture_id"], ["id"]
    )
    op.create_foreign_key("voting_user_id_fkey", "voting", "users", ["user_id"], ["id"])
    op.drop_constraint(None, "tickets", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "tickets_reservation_id_fkey",
        "tickets",
        "reservations",
        ["reservation_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "rooms", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "rooms_conference_id_fkey", "rooms", "conferences", ["conference_id"], ["id"]
    )
    op.drop_constraint(None, "reservations", schema="public", type_="foreignkey")
    op.drop_constraint(None, "reservations", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "reservations_user_id_fkey", "reservations", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "reservations_conference_id_fkey",
        "reservations",
        "conferences",
        ["conference_id"],
        ["id"],
    )
    op.drop_constraint(None, "questions", schema="public", type_="foreignkey")
    op.drop_constraint(None, "questions", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "questions_user_id_fkey", "questions", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "questions_lecture_id_fkey", "questions", "lectures", ["lecture_id"], ["id"]
    )
    op.drop_constraint(None, "lectures", schema="public", type_="foreignkey")
    op.drop_constraint(None, "lectures", schema="public", type_="foreignkey")
    op.drop_constraint(None, "lectures", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "lectures_lecturer_id_fkey",
        "lectures",
        "users",
        ["lecturer_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "lectures_room_id_fkey",
        "lectures",
        "rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "lectures_conference_id_fkey",
        "lectures",
        "conferences",
        ["conference_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "given_presentations", schema="public", type_="foreignkey")
    op.drop_constraint(None, "given_presentations", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "given_presentations_conference_id_fkey",
        "given_presentations",
        "conferences",
        ["conference_id"],
        ["id"],
    )
    op.create_foreign_key(
        "given_presentations_user_id_fkey",
        "given_presentations",
        "users",
        ["user_id"],
        ["id"],
    )
    op.drop_constraint(None, "conferences", schema="public", type_="foreignkey")
    op.drop_column("conferences", "organizer_id")
    # ### end Alembic commands ###