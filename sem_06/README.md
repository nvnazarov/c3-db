# Task 1

* Показать все названия книг вместе с именами издателей.

```sql
SELECT Title, PubName FROM Book;
```

* В какой книге наибольшее количество страниц?

```sql
SELECT ISBN FROM Book
WHERE PagesNum = max(PagesNum);
```

Если нужно только одну книгу, то в конце нужно добавить `LIMIT 1`.

* Какие авторы написали более 5 книг?

```sql
SELECT Author FROM Book GROUP BY Author
WHERE count() > 5;
```

* В каких книгах более чем в два раза больше страниц, чем среднее количество страниц для всех книг?

```sql
SELECT ISBN FROM Book WHERE PagesNum > 2*avg(PagesNum);
```

* Какие категории содержат подкатегории?

```sql
SELECT DISTINCT ParentCat from Category where ParentCat != null;
```

* У какого автора (предположим, что имена авторов уникальны) написано максимальное количество книг?

```sql
SELECT Author FROM Book GROUP BY Author WHERE ;
```

* Какие читатели забронировали все книги (не копии), написанные "Марком Твеном"?

```sql
SELECT 
```

* Какие книги имеют более одной копии?

```sql
SELECT ISBN FROM Copy GROUP BY ISBN WHERE count() > 1;
```

* ТОП 10 самых старых книг

```sql
SELECT ISBN FROM BOOK ORDER BY PubYear LIMIT 10; 
```

* Перечислите все категории в категории “Спорт” (с любым уровнем вложености).

```sql
WITH RECURSIVE SportSubcat AS (
    SELECT CategoryName FROM Category WHERE CategoryName = 'Спорт'
    UNION
    SELECT CategoryName FROM Category WHERE ParentCat IN SportSubcat
)
SELECT * FROM SportsSubcat;
```

# Task 2

* Добавьте запись о бронировании читателем ‘Василеем Петровым’ книги с ISBN 123456 и номером копии 4.

```sql
INSERT INTO Borrowing VALUES(
    (
        SELECT ReaderNr FROM Reader
        WHERE
            FirstName = 'Василий' AND
            LastName = 'Петров'
    ),
    '123456', 4, CURRENT_DATE
);
```

* Удалить все книги, год публикации которых превышает 2000 год.

```sql
DELETE FROM Book WHERE PubYear > 2000;
```

* Измените дату возврата для всех книг категории "Базы данных", начиная с 01.01.2016, чтобы они были в заимствовании на 30 дней дольше (предположим, что в SQL можно добавлять числа к датам).

```sql
UPDATE TABLE Borrowing
SET ReturnDate = ReturnDate + 30
WHERE ReturnDate >= '01.01.2016' AND ISBN IN (
    SELECT ISBN
    FROM BookCat
    WHERE CatergoryName = 'Базы данных'
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
SELECT * FROM Check c WHERE c.MatrNr = s.MatrNr AND c.Note >= 4.0 ) ;
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