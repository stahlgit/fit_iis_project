"""Datetime

Revision ID: c94efd825191
Revises: e6b5c72a45c9
Create Date: 2024-11-02 21:29:43.868252

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c94efd825191"
down_revision: Union[str, None] = "3e9df3b354c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the userrole enum
userrole_enum = postgresql.ENUM(
    "ADMIN", "REGISTERED", "GUEST", name="userrole", schema="public"
)


def upgrade() -> None:
    # Create the userrole enum type
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # Add new columns to conferences with a default value and make them non-nullable
    op.add_column(
        "conferences",
        sa.Column(
            "start_time", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "conferences",
        sa.Column(
            "end_time", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    # Foreign key adjustments for given_presentations
    op.drop_constraint(
        "given_presentations_conference_id_fkey",
        "given_presentations",
        type_="foreignkey",
    )
    op.drop_constraint(
        "given_presentations_user_id_fkey", "given_presentations", type_="foreignkey"
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
    op.create_foreign_key(
        None,
        "given_presentations",
        "conferences",
        ["conference_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )

    # Add new columns to lectures with default value and make them non-nullable
    op.add_column(
        "lectures",
        sa.Column(
            "start_time", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "lectures",
        sa.Column(
            "end_time", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    # Foreign key adjustments for lectures
    op.drop_constraint("lectures_lecturer_id_fkey", "lectures", type_="foreignkey")
    op.drop_constraint("lectures_conference_id_fkey", "lectures", type_="foreignkey")
    op.drop_constraint("lectures_room_id_fkey", "lectures", type_="foreignkey")
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
        "users",
        ["lecturer_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
        ondelete="CASCADE",
    )

    # Foreign key adjustments for questions
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

    # Alter the reservations table
    op.alter_column(
        "reservations", "user_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.drop_constraint(
        "reservations_conference_id_fkey", "reservations", type_="foreignkey"
    )
    op.drop_constraint("reservations_user_id_fkey", "reservations", type_="foreignkey")
    op.create_foreign_key(
        None,
        "reservations",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.create_foreign_key(
        None,
        "reservations",
        "conferences",
        ["conference_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )

    # Foreign key adjustments for rooms and tickets
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

    # Alter the users table to use the userrole enum
    op.execute(
        "ALTER TABLE public.users ALTER COLUMN role TYPE userrole USING role::userrole"
    )

    # Foreign key adjustments for voting
    op.drop_constraint("voting_user_id_fkey", "voting", type_="foreignkey")
    op.drop_constraint("voting_lecture_id_fkey", "voting", type_="foreignkey")
    op.create_foreign_key(
        None,
        "voting",
        "users",
        ["user_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )
    op.create_foreign_key(
        None,
        "voting",
        "lectures",
        ["lecture_id"],
        ["id"],
        source_schema="public",
        referent_schema="public",
    )


def downgrade() -> None:
    # Foreign key adjustments for voting
    op.drop_constraint(None, "voting", schema="public", type_="foreignkey")
    op.drop_constraint(None, "voting", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "voting_lecture_id_fkey", "voting", "lectures", ["lecture_id"], ["id"]
    )
    op.create_foreign_key("voting_user_id_fkey", "voting", "users", ["user_id"], ["id"])

    # Revert the role column type change in users table
    op.alter_column(
        "users",
        "role",
        existing_type=userrole_enum,
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    userrole_enum.drop(op.get_bind(), checkfirst=True)

    # Foreign key adjustments for tickets and rooms
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

    # Foreign key adjustments for reservations
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
    op.alter_column(
        "reservations", "user_id", existing_type=sa.INTEGER(), nullable=False
    )

    # Foreign key adjustments for questions
    op.drop_constraint(None, "questions", schema="public", type_="foreignkey")
    op.drop_constraint(None, "questions", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "questions_user_id_fkey", "questions", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "questions_lecture_id_fkey", "questions", "lectures", ["lecture_id"], ["id"]
    )

    # Revert changes to lectures
    op.drop_constraint(None, "lectures", schema="public", type_="foreignkey")
    op.drop_constraint(None, "lectures", schema="public", type_="foreignkey")
    op.drop_constraint(None, "lectures", schema="public", type_="foreignkey")
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
    op.create_foreign_key(
        "lectures_lecturer_id_fkey",
        "lectures",
        "users",
        ["lecturer_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("lectures", "end_time")
    op.drop_column("lectures", "start_time")

    # Foreign key adjustments for given_presentations
    op.drop_constraint(None, "given_presentations", schema="public", type_="foreignkey")
    op.drop_constraint(None, "given_presentations", schema="public", type_="foreignkey")
    op.create_foreign_key(
        "given_presentations_user_id_fkey",
        "given_presentations",
        "users",
        ["user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "given_presentations_conference_id_fkey",
        "given_presentations",
        "conferences",
        ["conference_id"],
        ["id"],
    )

    # Revert changes to conferences
    op.drop_column("conferences", "end_time")
    op.drop_column("conferences", "start_time")
