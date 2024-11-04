import models
import pprint

import sqlalchemy as sa
import sqlalchemy.orm as orm

DB_URI = "postgresql://superadmin:superadmin@localhost:5440/olymp"

# Для Олимпийских игр 2004 года сгенерируйте список (год рождения,
# количество игроков, количество золотых медалей), содержащий годы,
# в которые родились игроки, количество игроков, родившихся в каждый
# из этих лет, которые выиграли по крайней мере одну золотую медаль,
# и количество золотых медалей, завоеванных игроками, родившимися в этом году.
QUERY_1 = (
    sa.select(
        sa.extract("year", models.Athlete.birthdate),
        sa.func.count(sa.distinct(models.Athlete.id)),
        sa.func.count("*"),
    )
    .select_from(models.Athlete)
    .join(models.Result, models.Result.athlete_id == models.Athlete.id)
    .where(models.Result.medal == "GOLD")
    .group_by(sa.extract("year", models.Athlete.birthdate))
)

# Перечислите все индивидуальные (не групповые) соревнования, в которых
# была ничья в счете, и два или более игрока выиграли золотую медаль.
QUERY_2 = (
    sa.select(models.Event.id, models.Event.name)
    .where(models.Event.is_team_event == False)
    .where(
        sa.select(sa.func.count("*"))
        .select_from(models.Result)
        .where(models.Result.medal == "GOLD")
        .where(models.Result.event_id == models.Event.id)
        .scalar_subquery()
        >= 2
    )
)

# Найдите всех игроков, которые выиграли хотя бы одну медаль (GOLD,
# SILVER и BRONZE) на одной Олимпиаде. (player-name, olympic-id).
QUERY_3 = (
    sa.select(sa.distinct(models.Athlete.id), models.Event.olympics_id)
    .join(
        models.Result,
        models.Result.athlete_id == models.Athlete.id and models.Result.medal != None,
    )
    .join(models.Event, models.Event.id == models.Result.event_id)
)

# В какой стране был наибольший процент игроков (из перечисленных в
# наборе данных), чьи имена начинались с гласной?
QUERY_4 = (
    sa.select(models.Country.id, models.Country.name)
    .select_from(
        sa.select(
            models.Country.id,
            models.Country.name,
            sa.func.count("*").label("athletes_count"),
        )
        .join(models.Athlete, models.Athlete.country_id == models.Country.id)
        .group_by(models.Country.id)
        .subquery()
    )
    .join(models.Athlete, models.Athlete.country_id == models.Country.id)
    .where(models.Athlete.name.regexp_match(r"^[AOEIU]"))
    .group_by(models.Country.id)
    .order_by(sa.desc(sa.func.count("*") / "athletes_count"))
    .limit(1)
)

# Для Олимпийских игр 2000 года найдите 5 стран с минимальным соотношением
# количества групповых медалей к численности населения.
QUERY_5 = (
    sa.select(
        models.Country.name,
        (sa.func.count("*") / models.Country.population).label(
            "medals_population_proportion"
        ),
    )
    .select_from(models.Country)
    .join(models.Athlete, models.Athlete.country_id == models.Country.id)
    .join(
        models.Result,
        models.Result.athlete_id == models.Athlete.id and models.Result.medal != None,
    )
    .join(models.Event, models.Event.id == models.Result.event_id)
    .where(
        models.Event.olympics_id
        == (
            sa.select(models.Olympics.id)
            .where(models.Olympics.year == "2000")
            .scalar_subquery()
        )
    )
    .group_by(models.Country.id)
    .order_by(sa.asc("medals_population_proportion"))
    .limit(5)
)

engine = sa.create_engine(DB_URI)

for i, q in enumerate([QUERY_1, QUERY_2, QUERY_3, QUERY_4, QUERY_5]):
    print(f"\n### QUERY {i + 1} ###")
    try:
        with orm.Session(engine) as session:
            result = session.execute(q).all()
            if len(result) < 30:
                pprint.pp(result)
            else:
                pprint.pp(result, width=120, compact=True)
    except Exception as e:
        print(f"An error occured: {str(e).split("\n")[0]}")
