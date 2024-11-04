import argparse
import random
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm
import faker as fr

import models

EVENTS = [
    ("10000m Men", "ATH", "seconds", False, -1),
    ("10000m Women", "ATH", "seconds", False, -1),
    ("100m Backstroke Men", "ATH", "seconds", False, -1),
    ("100m Backstroke Women", "ATH", "seconds", False, -1),
    ("100m Breaststroke Men", "ATH", "seconds", False, -1),
    ("100m Breaststroke Women", "ATH", "seconds", False, -1),
    ("Hammer Throw Men", "ATH", "meters", False, -1),
    ("Hammer Throw Women", "ATH", "meters", False, -1),
    ("High Jump Men", "ATH", "meters", False, -1),
    ("High Jump Women", "ATH", "meters", False, -1),
    ("Long Jump Men", "ATH", "meters", False, -1),
    ("Long Jump Women", "ATH", "meters", False, -1),
    ("Shot Put Men", "ATH", "meters", False, -1),
    ("Shot Put Women", "ATH", "meters", False, -1),
]


def populate_db(n_athletes: int, n_events: int, seed: int, db: str):
    engine = sa.create_engine(db)

    with orm.Session(engine) as session:
        fr.Faker.seed(seed)
        random.seed(seed)

        faker = fr.Faker()

        countries = session.scalars(sa.select(models.Country)).all()
        olympics = session.scalars(sa.select(models.Olympics)).all()

        assert (
            len(countries) > 0
        ), "No countries in DB. Probably forgot to run migrations."
        assert (
            len(olympics) > 0
        ), "No olympics in DB. Probably forgot to run migrations."
        assert (
            len(EVENTS) >= n_events
        ), f"Max number of events (per olympiad) is {len(EVENTS)}, provided {n_events}."

        new_athlete = lambda is_male: models.Athlete(
            id=faker.sha256()[:10],
            name=(faker.name_male() if is_male else faker.name_female()),
            sex="WM"[int(is_male)],
            birthdate=faker.date_of_birth(minimum_age=16, maximum_age=60),
            country_id=countries[faker.random_int(0, len(countries) - 1)].id,
        )
        athletes = [new_athlete(faker.boolean(70)) for _ in range(n_athletes)]

        events = []
        shuffled_events = EVENTS.copy()
        for o in olympics:
            random.shuffle(shuffled_events)
            o_events = [
                models.Event(
                    id=faker.sha256()[:7],
                    name=e[0],
                    eventtype=e[1],
                    location=faker.address()[:50],
                    date=faker.date_between(
                        datetime(o.year, 1, 1), datetime(o.year + 1, 1, 1)
                    ),
                    olympics_id=o.id,
                    num_players_in_team=e[4],
                    result_noted_in=e[2],
                    is_team_event=e[3],
                )
                for e in shuffled_events[:n_events]
            ]
            events.extend(o_events)

        results = []
        men_athletes = list(filter(lambda a: a.sex == "M", athletes))
        women_athletes = list(filter(lambda a: a.sex == "W", athletes))
        is_men_event = lambda e: e.name.endswith("Men")
        for e in events:
            if e.is_team_event:
                continue

            e_athletes = (
                faker.random_elements(men_athletes, unique=True)
                if is_men_event(e)
                else faker.random_elements(women_athletes, unique=True)
            )
            e_results = [
                models.Result(
                    event_id=e.id,
                    athlete_id=a.id,
                    medal=None,
                    result=float(faker.random_int(1, 20)),
                    team_id=None,
                )
                for a in e_athletes
            ]

            e_results.sort(key=lambda x: x.result)
            if e.result_noted_in == "meters":
                e_results.reverse()

            medals = ["GOLD", "SILVER", "BRONZE"]
            medal_index = 0
            e_results[0].medal = "GOLD"
            for i in range(1, len(e_results)):
                if e_results[i - 1].result == e_results[i].result:
                    e_results[i].medal = e_results[i - 1].medal
                else:
                    medal_index += 1
                    if medal_index >= len(medals):
                        break
                    e_results[i].medal = medals[medal_index]

            results.extend(e_results)

        session.add_all(athletes)
        session.add_all(events)
        session.add_all(results)
        session.commit()

        print(
            "Successfully populated DB with "
            f"{n_athletes} athletes, "
            f"{n_events * len(olympics)} events and "
            f"{len(results)} results."
        )


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seeder.py",
        description="Populates DB with fake data.",
    )
    parser.add_argument(
        "-a",
        "--athletes",
        dest="n_athletes",
        type=int,
        default=len(EVENTS) * 6,
        metavar="N",
        help="Number of athletes.",
    )
    parser.add_argument(
        "-e",
        "--events",
        dest="n_events",
        type=int,
        default=len(EVENTS),
        metavar="N",
        help="Number of events per olympiad.",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=0,
        metavar="N",
        help="Seed used to generate fake data.",
    )
    parser.add_argument(
        "--db",
        default="postgresql://superadmin:superadmin@localhost:5440/olymp",
        help="DB URI.",
    )
    return parser


if __name__ == "__main__":
    args = setup_parser().parse_args().__dict__
    populate_db(**args)
