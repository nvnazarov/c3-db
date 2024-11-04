"""Create tables.

Revision ID: 030ddd966fb8
Revises: 
Create Date: 2024-10-30 19:41:37.308645

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "030ddd966fb8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "countries",
        sa.Column("id", sa.String(3)),
        sa.Column("name", sa.String(40)),
        sa.Column("area_sqkm", sa.Integer()),
        sa.Column("population", sa.Integer()),
        sa.PrimaryKeyConstraint("id", name="pk_countries_id"),
    )
    op.create_table(
        "olympics",
        sa.Column("id", sa.String(7)),
        sa.Column(
            "country_id",
            sa.String(3),
            sa.ForeignKey("countries.id", name="fk_olympics_county_id"),
        ),
        sa.Column("city", sa.String(50)),
        sa.Column("year", sa.Integer()),
        sa.Column("season", sa.String(6)),
        sa.CheckConstraint("season IN ('summer', 'winter')", name="cc_olympics_season"),
        sa.PrimaryKeyConstraint("id", name="pk_olympics_id"),
    )
    op.create_table(
        "athletes",
        sa.Column("id", sa.String(10)),
        sa.Column("name", sa.String(40)),
        sa.Column("sex", sa.CHAR, nullable=True),
        sa.Column("birthdate", sa.Date()),
        sa.Column(
            "country_id",
            sa.String(3),
            sa.ForeignKey("countries.id", name="fk_athletes_country_id"),
        ),
        sa.CheckConstraint("sex IN ('M', 'W')", name="cc_athletes_sex"),
        sa.PrimaryKeyConstraint("id", name="pk_athletes_id"),
    )
    op.create_table(
        "events",
        sa.Column("id", sa.String(7)),
        sa.Column("name", sa.String(40)),
        sa.Column("eventtype", sa.String(20)),
        sa.Column("location", sa.String(50)),
        sa.Column("date", sa.DateTime()),
        sa.Column(
            "olympics_id",
            sa.String(7),
            sa.ForeignKey("olympics.id", name="fk_events_olympic_id"),
        ),
        sa.Column(
            "is_team_event",
            sa.Boolean(create_constraint=True, name="cc_events_is_team_event"),
        ),
        sa.Column("num_players_in_team", sa.Integer()),
        sa.Column("result_noted_in", sa.String(100)),
        sa.PrimaryKeyConstraint("id", name="pk_events_id"),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer()),
        sa.Column("name", sa.String(50)),
        sa.Column(
            "event_id",
            sa.String(7),
            sa.ForeignKey("events.id", name="fk_teams_event_id"),
        ),
        sa.PrimaryKeyConstraint("id", name="pk_teams"),
    )
    op.create_table(
        "results",
        sa.Column(
            "event_id",
            sa.String(7),
            sa.ForeignKey("events.id", name="fk_results_event_id"),
        ),
        sa.Column(
            "athlete_id",
            sa.String(10),
            sa.ForeignKey("athletes.id", name="fk_results_athlete_id"),
        ),
        sa.Column("medal", sa.String(7), nullable=True),
        sa.Column("result", sa.Double()),
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", name="fk_results_team_id"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("event_id", "athlete_id", name="pk_results"),
    )


def downgrade() -> None:
    op.drop_table("results", if_exists=True)
    op.drop_table("teams", if_exists=True)
    op.drop_table("events", if_exists=True)
    op.drop_table("athletes", if_exists=True)
    op.drop_table("olympics", if_exists=True)
    op.drop_table("countries", if_exists=True)
