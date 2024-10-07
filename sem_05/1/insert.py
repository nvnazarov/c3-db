import re
import random
import itertools
from datetime import datetime, timedelta
from dataclasses import dataclass

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://student:student@localhost:5433/db")

ADDRESSES = ["Moscow", *[s for s in "abcdefg"]]
AUTHORS = [s for s in "abcdefg"]


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


def generate_random_inserts(seed=None):
    if seed:
        random.seed(seed)

    rand = lambda: random.randint(1, 100)

    readers = [
        {
            "ID": i,
            "LastName": f"reader-{i}",
            "FirstName": f"reader-{i}",
            "Address": random.choice(ADDRESSES),
            "BirthDate": None,
        }
        for i in range(10)
    ]

    readers.append(
        {
            "ID": 10,
            "LastName": f"Иванов",
            "FirstName": f"Иван",
            "Address": random.choice(ADDRESSES),
            "BirthDate": None,
        }
    )

    publishers = [
        {
            "PubName": f"publisher-{i}",
            "PubAdress": f"address-{i}",
        }
        for i in range(10)
    ]

    books = [
        {
            "ISBN": f"isbn-{i}",
            "Title": f"title-{i}",
            "Author": random.choice(AUTHORS),
            "PagesNum": rand(),
            "PubYear": rand(),
            "PubName": random.choice(publishers)["PubName"],
        }
        for i in range(10)
    ]

    categories = [
        {
            "CategoryName": "Горы",
            "ParentCat": None,
        },
        {
            "CategoryName": "Путешествия",
            "ParentCat": None,
        },
        *[
            {
                "CategoryName": f"cat-{i}",
                "ParentCat": None,
            }
            for i in range(5)
        ]
    ]

    copies = [
        {
            "ISBN": isbn,
            "CopyNumber": i,
            "ShelfPosition": rand(),
        }
        for i, isbn in itertools.product(range(4), map(lambda x: x["ISBN"], books))
    ]

    borrowings = [
        {
            "ReaderNr": random.choice(readers)["ID"],
            "ISBN": random.choice(books)["ISBN"],
            "CopyNumber": random.randint(0,3),
            "ReturnDate": datetime.now() - timedelta(days=7) + timedelta(days=i),
        }
        for i in range(15)
    ]

    books_with_cats = random.sample(books, 6)
    rand_cats = lambda: random.sample(categories, random.randint(1, len(categories)))
    bc = [
        [
            {
                "ISBN": book["ISBN"],
                "CategoryName": c["CategoryName"],
            }
            for c in cats
        ]
        for book, cats in zip(books_with_cats, [rand_cats() for i in range(len(books_with_cats))])
    ]
    book_cat = []
    for x in bc:
        book_cat.extend(x)
    
    return {
        "Reader": readers,
        "Book": books,
        "Publisher": publishers,
        "Category": categories,
        "Copy": copies,
        "Borrowing": borrowings,
        "BookCat": book_cat,
    }


TABLES = list(
    map(
        Table.from_signature,
        [
            "Reader(ID,LastName,FirstName,Address,BirthDate)",
            "Publisher(PubName,PubAdress)",
            "Book(ISBN,Title,Author,PagesNum,PubYear,PubName)",
            "Category(CategoryName,ParentCat)",
            "Copy(ISBN,CopyNumber,ShelfPosition)",
            "Borrowing(ReaderNr,ISBN,CopyNumber,ReturnDate)",
            "BookCat(ISBN,CategoryName)",
        ],
    )
)

data = generate_random_inserts(2)

with engine.connect() as conn:
    for table in TABLES:
        conn.execute(
            text(f"INSERT INTO {table.signature} VALUES {table.params}"),
            data[table.name],
        )
    conn.commit()
