import re
import random
import itertools
from datetime import datetime, timedelta
from dataclasses import dataclass

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://student:student@localhost:5433/db")

@dataclass
class Table:
    name: str
    attributes: list[str]

    @staticmethod
    def from_signature(s):
        match = re.match(r"(\w+)\(((?:\w+\,)*\w+)\)", s)
        return Table(name=match[1], attributes=match[2].split(","))
    
    @property
    def signature(self):
        return f"{self.name}({",".join(self.attributes)})"

    @property
    def params(self):
        return f"({",".join(map(lambda a: f":{a}", self.attributes))})"


def generate_random_inserts(seed):
    if seed:
        random.seed(seed)

    rand = lambda: random.randint(1, 100)

    CITIES = [("Moscow", "Moscow"), ("St.Petersburg", "St.Petersburg"), ("Tver", "Tver")]

    cities = [
        {
            "Name": city[0],
            "Region": city[1],
        }
        for city in CITIES
    ]

    stations = [
        {
            "Name": f"station-{i}",
            "Tracks": rand(),
            "CityName": city[0],
            "Region": city[1],
        }
        for i, city in enumerate(CITIES)
    ]

    TRAIN_START_END_STATIONS = [
        ("station-0", "station-1"),
        ("station-1", "station-2"),
        ("station-2", "station-2"),
    ] 

    trains = [
        {
            "TrainNr": i,
            "Length": rand(),
            "StartStationName": TRAIN_START_END_STATIONS[i][0],
            "EndStationName": TRAIN_START_END_STATIONS[i][1],
        }
        for i in range(3)
    ]

    now = datetime.now()
    CONNECTIONS = [
        ("station-0", "station-2", 0, now, now + timedelta(1)),
        ("station-2", "station-1", 0, now + timedelta(1), now + timedelta(2)),
        ("station-0", "station-1", 0, now, now + timedelta(2)),

        ("station-1", "station-2", 1, now, now + timedelta(1)),
        
        ("station-2", "station-0", 2, now, now + timedelta(1)),
        ("station-0", "station-1", 2, now + timedelta(1), now + timedelta(days=1, hours=4)),
        ("station-1", "station-2", 2, now + timedelta(2), now + timedelta(3)),
        ("station-2", "station-1", 2, now, now + timedelta(days=1, hours=4)),
        ("station-2", "station-2", 2, now, now + timedelta(3)),
        ("station-0", "station-2", 2, now + timedelta(1), now + timedelta(3)),
    ]

    connections = [
        {
            "FromStation": c[0],
            "ToStation": c[1],
            "TrainNr": c[2],
            "Departure": c[3],
            "Arrival": c[4],
        }
        for c in CONNECTIONS
    ]
    
    return {
        "City": cities,
        "Station": stations,
        "Train": trains,
        "Connection": connections,
    }


TABLES = list(
    map(
        Table.from_signature,
        [
            "City(Name,Region)",
            "Station(Name,Tracks,CityName,Region)",
            "Train(TrainNr,Length,StartStationName,EndStationName)",
            "Connection(FromStation,ToStation,TrainNr,Departure,Arrival)",
        ],
    )
)

data = generate_random_inserts(0)

with engine.connect() as conn:
    for table in TABLES:
        conn.execute(
            text(f"INSERT INTO {table.signature} VALUES {table.params}"),
            data[table.name],
        )
    conn.commit()
