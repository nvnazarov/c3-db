begin;

create table if not exists city(
    id integer primary key,
    name varchar,
    region varchar
);

create table if not exists station(
    id integer primary key,
    name varchar,
    n_tracks integer,
    city_id integer references city(id)
);

create table if not exists train(
    id integer primary key,
    len integer,
    start_station_id integer references station(id),
    end_station_id integer references station(id)
);

create table if not exists connected(
    id integer primary key,
    from_station_id integer references station(id),
    to_station_id integer references station(id),
    departure timestamp,
    arrival timestamp
);

create table if not exists train_connected(
    id integer primary key,
    train_id integer references train(id),
    connected_id integer references connected(id)
);

commit;