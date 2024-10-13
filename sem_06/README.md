# Task 1

* Показать все названия книг вместе с именами издателей.

```sql
SELECT title, publisher_name FROM book;
```

* В какой книге наибольшее количество страниц?

```sql
SELECT ISBN, Title, number_of_pages FROM book
WHERE number_of_pages = (SELECT MAX(number_of_pages) FROM book);
```

Если нужно только одну книгу, то в конце нужно добавить `LIMIT 1`.

* Какие авторы написали более 5 книг?

```sql
SELECT author FROM book GROUP BY author HAVING COUNT(*) > 5;
```

* В каких книгах более чем в два раза больше страниц, чем среднее количество страниц для всех книг?

```sql
SELECT isbn FROM book WHERE number_of_pages > 2*(SELECT AVG(number_of_pages) FROM book);
```

* Какие категории содержат подкатегории?

```sql
SELECT DISTINCT parentcat FROM category WHERE parentcat IS NOT NULL;
```

* У какого автора (предположим, что имена авторов уникальны) написано максимальное количество книг?

```sql
WITH author_books_count AS (
    SELECT author, COUNT(*) AS books_count FROM book GROUP BY author
)
SELECT * FROM author_books_count
WHERE books_count = (SELECT MAX(books_count) FROM author_books_count);
```

* Какие читатели забронировали все книги (не копии), написанные "Марком Твеном"?

```sql
WITH mark_books_readers AS (
    SELECT DISTINCT br.id, b.isbn
    FROM borrowing br
        JOIN book b ON b.isbn = br.isbn
    WHERE b.author = 'Марк Твен'
)
SELECT id FROM mark_books_readers GROUP BY id
HAVING COUNT(*) = (SELECT COUNT(*) FROM book WHERE author = 'Марк Твен');
```

* Какие книги имеют более одной копии?

```sql
SELECT isbn, COUNT(*) as number_of_copies FROM copy GROUP BY isbn HAVING COUNT(*) > 1;
```

* ТОП 10 самых старых книг

```sql
SELECT isbn, year FROM book ORDER BY year LIMIT 10;
```

* Перечислите все категории в категории “Спорт” (с любым уровнем вложености).

```sql
WITH RECURSIVE sport_subcats(categoryname) AS (
    VALUES ('Спорт')
    UNION
    SELECT c.categoryname
    FROM sport_subcats ss
    JOIN category c ON ss.categoryname = c.parentcat
)
SELECT * FROM sport_subcats;
```

# Task 2

* Добавьте запись о бронировании читателем ‘Василеем Петровым’ книги с ISBN 123456 и номером копии 4.

```sql
INSERT INTO borrowing
VALUES
(
    (
        SELECT id FROM reader
        WHERE
            firstname = 'Василий' AND
            lastname = 'Петров'
    ),
    '123456', 4, CURRENT_DATE
);
```

* Удалить все книги, год публикации которых превышает 2000 год.

```sql
DELETE FROM book WHERE year > 2000;
```

* Измените дату возврата для всех книг категории "Базы данных", начиная с 01.01.2016, чтобы они были в заимствовании на 30 дней дольше (предположим, что в SQL можно добавлять числа к датам).

```sql
UPDATE borrowing
SET returndate = returndate + 30
WHERE returndate >= '01.01.2016' AND isbn IN (
    SELECT isbn
    FROM bookcategory
    WHERE categoryname = 'Базы данных'
);
```

# Task 3

Рассмотрим следующую реляционную схему:

* Student(MatrNr, Name, Semester)
* Check(MatrNr, LectNr, ProfNr, Note)
* Lecture(LectNr, Title, Credit, ProfNr)
* Professor(ProfNr, Name, Room)

Опишите на русском языке результаты следующих запросов:

1.
```sql
SELECT s.Name, s.MatrNr FROM Student s
WHERE NOT EXISTS (
SELECT * FROM Check c WHERE c.MatrNr = s.MatrNr AND c.Note >= 4.0 );
```

Студенты (имя и MatrNr), которые никогда не получали оценку $\ge 4.0$. 

2.
```sql
( SELECT p.ProfNr, p.Name, sum(lec.Credit)
FROM Professor p, Lecture lec
WHERE p.ProfNr = lec.ProfNr
GROUP BY p.ProfNr, p.Name)
UNION
( SELECT p.ProfNr, p.Name, 0
FROM Professor p
WHERE NOT EXISTS (
SELECT * FROM Lecture lec WHERE lec.ProfNr = p.ProfNr ));
```

Для каждого профессора выводится его имя, ProfNr и сумма кредитов всех лекций, которые он ведет (0, если профессор не ведет ни одну лекцию).

3.
```sql
SELECT s.Name, p.Note
FROM Student s, Lecture lec, Check c
WHERE s.MatrNr = c.MatrNr AND lec.LectNr = c.LectNr AND c.Note >= 4
AND c.Note >= ALL (
SELECT c1.Note FROM Check c1 WHERE c1.MatrNr = c.MatrNr )
```

Для каждого студента выводится его имя и самые высокие оценки, не меньшие $4.0$ (то есть те оценки, которые равны максимуму из всех оценок этого студента, при условии, что максимум $>= 4.0$).