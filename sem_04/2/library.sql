begin;

create table if not exists publisher(
    id integer primary key,
    name varchar not null,
    address varchar not null
);

create table if not exists book(
    id integer primary key,
    isbn varchar,
    year integer,
    title varchar,
    author varchar,
    pages integer,
    publisher_id integer references publisher(id)
);

create table if not exists copy(
    id integer primary key,
    location varchar,
    book_id integer references book(id)
);

create table if not exists category(
    id integer primary key,
    name varchar,
    parent_category_id integer references category(id)
);

create table if not exists book_category(
    id integer primary key,
    book_id integer references book(id),
    category_id integer references category(id)
);

create table if not exists reader(
    id integer primary key,
    name varchar,
    surname varchar,
    address varchar,
    birthday timestamp
);

create table if not exists copy_reader(
    id integer primary key,
    reader_id integer references reader(id),
    copy_id integer references copy(id),
    return_date timestamp
);

commit;