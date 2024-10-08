begin;

create table if not exists City(
    Name varchar not null,
    Region varchar not null,
    primary key (Name, Region)
);

create table if not exists Station(
    Name varchar primary key,
    Tracks integer not null,
    CityName varchar not null,
    Region varchar not null
);

create table if not exists Train(
    TrainNr integer primary key,
    Length integer not null,
    StartStationName varchar not null references Station(Name),
    EndStationName varchar not null references Station(Name)
);

create table if not exists Connection(
    FromStation varchar not null references Station(Name),
    ToStation varchar not null references Station(Name),
    TrainNr integer not null references Train(TrainNr),
    Departure timestamp,
    Arrival timestamp
);

commit;