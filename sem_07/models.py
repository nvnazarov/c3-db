from datetime import datetime

import sqlalchemy.orm as orm


_mc = orm.mapped_column

_int = orm.Mapped[int]
_str = orm.Mapped[str]
_float = orm.Mapped[float]
_bool = orm.Mapped[bool]
_datetime = orm.Mapped[datetime]


class Base(orm.DeclarativeBase):
    type_annotation_map = {}


class Country(Base):
    __tablename__ = "countries"
    id: _str = _mc(primary_key=True)
    name: _str
    area_sqkm: _int
    population: _int


class Olympics(Base):
    __tablename__ = "olympics"
    id: _str = _mc(primary_key=True)
    country_id: _str
    city: _str
    year: _int
    season: _str


class Athlete(Base):
    __tablename__ = "athletes"
    id: _str = _mc(primary_key=True)
    name: _str
    sex: _str
    birthdate: _datetime
    country_id: _str


class Event(Base):
    __tablename__ = "events"
    id: _str = _mc(primary_key=True)
    name: _str
    eventtype: _str
    location: _str
    date: _datetime
    olympics_id: _str
    is_team_event: _bool
    num_players_in_team: _int
    result_noted_in: _str


class Result(Base):
    __tablename__ = "results"
    event_id: _str = _mc(primary_key=True)
    athlete_id: _str = _mc(primary_key=True)
    medal: orm.Mapped[str | None]
    result: _float
    team_id: orm.Mapped[int | None]


class Team(Base):
    __tablename__ = "teams"
    id: _int = _mc(primary_key=True)
    name: _str
    event_id: _str
