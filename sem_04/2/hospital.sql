begin;

create table if not exists station(
    id integer primary key,
    name varchar
);

create table if not exists room(
    id integer primary key,
    station_id integer not null references station(id),
    n_beds integer
);

create table if not exists station_personell(
    id integer primary key,
    name varchar,
    works_for integer references station(id)
);

create table if not exists caregiver(
    id integer primary key references station_personell(id),
    qualification varchar
);

create table if not exists doctor(
    id integer primary key references station_personell(id),
    area varchar,
    rank varchar
);

create table if not exists patient(
    id integer primary key,
    name varchar,
    disease varchar,
    treated_by integer references doctor(id),
    room_id integer references room(id),
    from_date timestamp,
    to_date timestamp
);

commit;