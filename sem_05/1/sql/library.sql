begin;

create table if not exists Reader(
    ID integer primary key,
    LastName varchar not null,
    FirstName varchar not null,
    Address varchar not null,
    BirthDate date
);

create table if not exists Publisher(
    PubName varchar primary key,
    PubAdress varchar not null
);

create table if not exists Book(
    ISBN varchar primary key,
    Title varchar not null,
    Author varchar not null,
    PagesNum integer not null,
    PubYear integer not null,
    PubName varchar not null references Publisher(PubName)
);

create table if not exists Category(
    CategoryName varchar primary key,
    ParentCat varchar
);

create table if not exists Copy(
    ISBN varchar references Book(ISBN),
    CopyNumber integer not null,
    ShelfPosition integer,
    primary key (ISBN, CopyNumber)
);

create table if not exists Borrowing(
    ReaderNr integer,
    ISBN varchar references Book(ISBN),
    CopyNumber varchar,
    ReturnDate date,
    primary key (ReaderNr, ISBN, CopyNumber, ReturnDate)
);

create table if not exists BookCat(
    ISBN varchar references Book(ISBN) not null,
    CategoryName varchar references Category(CategoryName) not null,
    primary key (ISBN, CategoryName)
);

commit;