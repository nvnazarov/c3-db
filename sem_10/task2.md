# Задание 2: Специальные случаи использования индексов

# Партиционирование и специальные случаи использования индексов

1. Удалите прошлый инстанс PostgreSQL - `docker-compose down` в папке `src` и запустите новый: `docker-compose up -d`.

2. Создайте партиционированную таблицу и заполните её данными:

    ```sql
    -- Создание партиционированной таблицы
    CREATE TABLE t_books_part (
        book_id     INTEGER      NOT NULL,
        title       VARCHAR(100) NOT NULL,
        category    VARCHAR(30),
        author      VARCHAR(100) NOT NULL,
        is_active   BOOLEAN      NOT NULL
    ) PARTITION BY RANGE (book_id);

    -- Создание партиций
    CREATE TABLE t_books_part_1 PARTITION OF t_books_part
        FOR VALUES FROM (MINVALUE) TO (50000);

    CREATE TABLE t_books_part_2 PARTITION OF t_books_part
        FOR VALUES FROM (50000) TO (100000);

    CREATE TABLE t_books_part_3 PARTITION OF t_books_part
        FOR VALUES FROM (100000) TO (MAXVALUE);

    -- Копирование данных из t_books
    INSERT INTO t_books_part 
    SELECT * FROM t_books;
    ```

3. Обновите статистику таблиц:
    ```sql
    ANALYZE t_books;
    ANALYZE t_books_part;
    ```
   
    *Результат:*
    ```
    workshop=# ANALYZE t_books;
       ANALYZE t_books_part;
    ANALYZE
    ANALYZE
    ```

4. Выполните запрос для поиска книги с id = 18:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books_part WHERE book_id = 18;
    ```
    
    *План выполнения:*
    ```
     Seq Scan on t_books_part_1 t_books_part  (cost=0.00..1032.99 rows=1 width=32) (actual time=0.006..2.609 rows=1 loops=1)
       Filter: (book_id = 18)
       Rows Removed by Filter: 49998
     Planning Time: 0.119 ms
     Execution Time: 2.624 ms
    (5 rows)
    ```
    
    *Объясните результат:*
    
    `Seq Scan` по первой партиции (с `book_id` в (`MINVALUE`, 50000)), поскольку ищем книгу с `book_id = 18`. 

5. Выполните поиск по названию книги:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books_part 
    WHERE title = 'Expert PostgreSQL Architecture';
    ```
   
    *План выполнения:*
    ```
     Append  (cost=0.00..3101.01 rows=3 width=33) (actual time=3.455..9.096 rows=1 loops=1)
       ->  Seq Scan on t_books_part_1  (cost=0.00..1032.99 rows=1 width=32) (actual time=3.454..3.454 rows=1 loops=1)
             Filter: ((title)::text = 'Expert PostgreSQL Architecture'::text)
             Rows Removed by Filter: 49998
       ->  Seq Scan on t_books_part_2  (cost=0.00..1034.00 rows=1 width=33) (actual time=2.836..2.836 rows=0 loops=1)
             Filter: ((title)::text = 'Expert PostgreSQL Architecture'::text)
             Rows Removed by Filter: 50000
       ->  Seq Scan on t_books_part_3  (cost=0.00..1034.01 rows=1 width=34) (actual time=2.802..2.802 rows=0 loops=1)
             Filter: ((title)::text = 'Expert PostgreSQL Architecture'::text)
             Rows Removed by Filter: 50001
     Planning Time: 0.315 ms
     Execution Time: 9.397 ms
    (12 rows)
    ```
   
   *Объясните результат:*
   
    Поскольку неизвестно, в какой партиции находятся объекты с `title = 'Expert PostgreSQL Architecture'`, то проходимся методом `Seq Scan` по всем партициям, а потом собираем все результаты через `Append`.

6. Создайте партиционированный индекс:
    ```sql
    CREATE INDEX ON t_books_part(title);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX ON t_books_part(title);
    CREATE INDEX
    ```

7. Повторите запрос из шага 5:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books_part 
    WHERE title = 'Expert PostgreSQL Architecture';
    ```
    
    *План выполнения:*
    ```
     Append  (cost=0.29..24.94 rows=3 width=33) (actual time=0.021..0.050 rows=1 loops=1)
       ->  Index Scan using t_books_part_1_title_idx on t_books_part_1  (cost=0.29..8.31 rows=1 width=32) (actual time=0.020..0.020 rows=1 loops=1)
             Index Cond: ((title)::text = 'Expert PostgreSQL Architecture'::text)
       ->  Index Scan using t_books_part_2_title_idx on t_books_part_2  (cost=0.29..8.31 rows=1 width=33) (actual time=0.015..0.015 rows=0 loops=1)
             Index Cond: ((title)::text = 'Expert PostgreSQL Architecture'::text)
       ->  Index Scan using t_books_part_3_title_idx on t_books_part_3  (cost=0.29..8.31 rows=1 width=34) (actual time=0.013..0.013 rows=0 loops=1)
             Index Cond: ((title)::text = 'Expert PostgreSQL Architecture'::text)
     Planning Time: 0.300 ms
     Execution Time: 0.065 ms
    (9 rows)
    ```
    
    *Объясните результат:*

    Теперь можно проходиться по всем партициям не методом `Seq Scan`, а `Index Scan`. Это значительно ускорило выполнение запроса.

8. Удалите созданный индекс:
    ```sql
    DROP INDEX t_books_part_title_idx;
    ```
   
    *Результат:*
    ```
    workshop=# DROP INDEX t_books_part_title_idx;
    DROP INDEX
    ```

9. Создайте индекс для каждой партиции:
    ```sql
    CREATE INDEX ON t_books_part_1(title);
    CREATE INDEX ON t_books_part_2(title);
    CREATE INDEX ON t_books_part_3(title);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX ON t_books_part_1(title);
        CREATE INDEX ON t_books_part_2(title);
        CREATE INDEX ON t_books_part_3(title);
    CREATE INDEX
    CREATE INDEX
    CREATE INDEX
    ```

10. Повторите запрос из шага 5:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books_part 
    WHERE title = 'Expert PostgreSQL Architecture';
    ```
    
    *План выполнения:*
    ```
     Append  (cost=0.29..24.94 rows=3 width=33) (actual time=0.012..0.025 rows=1 loops=1)
       ->  Index Scan using t_books_part_1_title_idx on t_books_part_1  (cost=0.29..8.31 rows=1 width=32) (actual time=0.011..0.011 rows=1 loops=1)
             Index Cond: ((title)::text = 'Expert PostgreSQL Architecture'::text)
       ->  Index Scan using t_books_part_2_title_idx on t_books_part_2  (cost=0.29..8.31 rows=1 width=33) (actual time=0.006..0.006 rows=0 loops=1)
             Index Cond: ((title)::text = 'Expert PostgreSQL Architecture'::text)
       ->  Index Scan using t_books_part_3_title_idx on t_books_part_3  (cost=0.29..8.31 rows=1 width=34) (actual time=0.006..0.006 rows=0 loops=1)
             Index Cond: ((title)::text = 'Expert PostgreSQL Architecture'::text)
     Planning Time: 0.314 ms
     Execution Time: 0.039 ms
    (9 rows)
    ```
    
    *Объясните результат:*
    
    Похоже, что ничего не изменилось. Похоже `CREATE INDEX` для партицированной таблицы по умолчанию создает индексы для каждой партиции.

11. Удалите созданные индексы:
    ```sql
    DROP INDEX t_books_part_1_title_idx;
    DROP INDEX t_books_part_2_title_idx;
    DROP INDEX t_books_part_3_title_idx;
    ```
    
    *Результат:*
    ```
    workshop=# DROP INDEX t_books_part_1_title_idx;
        DROP INDEX t_books_part_2_title_idx;
        DROP INDEX t_books_part_3_title_idx;
    DROP INDEX
    DROP INDEX
    DROP INDEX
    ```

12. Создайте обычный индекс по book_id:
    ```sql
    CREATE INDEX t_books_part_idx ON t_books_part(book_id);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX t_books_part_idx ON t_books_part(book_id);
    CREATE INDEX
    ```

13. Выполните поиск по book_id:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books_part WHERE book_id = 11011;
    ```
    
    *План выполнения:*
    ```
     Index Scan using t_books_part_1_book_id_idx on t_books_part_1 t_books_part  (cost=0.29..8.31 rows=1 width=32) (actual time=0.009..0.010 rows=1 loops=1)
       Index Cond: (book_id = 11011)
     Planning Time: 0.191 ms
     Execution Time: 0.020 ms
    (4 rows)
    ```
    
    *Объясните результат:*

    PostgreSQL понял, что `book_id = 11011` надо искать в первой партиции, и использует индекс оп PK `book_id`. При этом общий индекс, который мы создали, видимо, игнорируется.

14. Создайте индекс по полю is_active:
    ```sql
    CREATE INDEX t_books_active_idx ON t_books(is_active);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX t_books_active_idx ON t_books(is_active);
    CREATE INDEX
    ```

15. Выполните поиск активных книг с отключенным последовательным сканированием:
    ```sql
    SET enable_seqscan = off;
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE is_active = true;
    SET enable_seqscan = on;
    ```
    
    *План выполнения:*
    ```
     Bitmap Heap Scan on t_books  (cost=841.58..2816.63 rows=75005 width=33) (actual time=1.627..7.344 rows=74766 loops=1)
       Recheck Cond: is_active
       Heap Blocks: exact=1225
       ->  Bitmap Index Scan on t_books_active_idx  (cost=0.00..822.83 rows=75005 width=0) (actual time=1.521..1.521 rows=74766 loops=1)
             Index Cond: (is_active = true)
     Planning Time: 0.207 ms
     Execution Time: 9.174 ms
    (7 rows)
    ```
    
    *Объясните результат:*
    
    Поскольку мы отключили `Seq Scan`, PostgreSQL вынужден использовать индекс по `is_active`. Он решил сделать это с помощью метода `Bitmap Index Scan` (поскольку может быть много строк с `is_active = true`).

16. Создайте составной индекс:
    ```sql
    CREATE INDEX t_books_author_title_index ON t_books(author, title);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX t_books_author_title_index ON t_books(author, title);
    CREATE INDEX
    ```

17. Найдите максимальное название для каждого автора:
    ```sql
    EXPLAIN ANALYZE
    SELECT author, MAX(title) 
    FROM t_books 
    GROUP BY author;
    ```
    
    *План выполнения:*
    ```
     HashAggregate  (cost=3475.00..3485.00 rows=1000 width=42) (actual time=44.502..44.607 rows=1003 loops=1)
       Group Key: author
       Batches: 1  Memory Usage: 193kB
       ->  Seq Scan on t_books  (cost=0.00..2725.00 rows=150000 width=21) (actual time=0.004..7.224 rows=150000 loops=1)
     Planning Time: 0.322 ms
     Execution Time: 44.657 ms
    (6 rows)
    ```
    
    *Объясните результат:*
    
    PostgreSQL использовал `HashAggregate` для реализации `GROUP BY`. Данные `HashAggregate` получает последовательным проходом по всей таблице (`Seq Scan`). Также `HashAggregate` поддерживает `MAX(title)` для каждого ключа и обновляет его по поступлении новых данных.

18. Выберите первых 10 авторов:
    ```sql
    EXPLAIN ANALYZE
    SELECT DISTINCT author 
    FROM t_books 
    ORDER BY author 
    LIMIT 10;
    ```
    
    *План выполнения:*
    ```
    Limit  (cost=0.42..56.67 rows=10 width=10) (actual time=0.021..0.188 rows=10 loops=1)
       ->  Result  (cost=0.42..5625.42 rows=1000 width=10) (actual time=0.020..0.186 rows=10 loops=1)
             ->  Unique  (cost=0.42..5625.42 rows=1000 width=10) (actual time=0.019..0.185 rows=10 loops=1)
                   ->  Index Only Scan using t_books_author_title_index on t_books  (cost=0.42..5250.42 rows=150000 width=10) (actual time=0.019..0.114 rows=1370 loops=1)
                         Heap Fetches: 0
     Planning Time: 0.339 ms
     Execution Time: 0.222 ms
    (7 rows)
    ```
    
    *Объясните результат:*
    
    PostgreSQL использует `Index Only Scan`, поскольку в `SELECT` выбирается только колонка `author`, которая и используется в `t_books_author_title_index`. Поскольку выбираются `DISTINCT author`, то PostgreSQL использует фильтр `Unique`. После этого берутся 10 первых строки с помощью `Limit`.

19. Выполните поиск и сортировку:
    ```sql
    EXPLAIN ANALYZE
    SELECT author, title 
    FROM t_books 
    WHERE author LIKE 'T%'
    ORDER BY author, title;
    ```
    
    *План выполнения:*
    ```
     Sort  (cost=3100.29..3100.33 rows=15 width=21) (actual time=12.231..12.232 rows=1 loops=1)
       Sort Key: author, title
       Sort Method: quicksort  Memory: 25kB
       ->  Seq Scan on t_books  (cost=0.00..3100.00 rows=15 width=21) (actual time=12.209..12.210 rows=1 loops=1)
             Filter: ((author)::text ~~ 'T%'::text)
             Rows Removed by Filter: 149999
     Planning Time: 1.215 ms
     Execution Time: 12.246 ms
    (8 rows)
    ```
    
    *Объясните результат:*
    
    Поскольку осуществляется поиск по паттерну, то используется `Seq Scan` (у нас нет индексов типа `GIN` на колонке `author`). После этого применяется сортировка методом `quicksort`.

20. Добавьте новую книгу:
    ```sql
    INSERT INTO t_books (book_id, title, author, category, is_active)
    VALUES (150001, 'Cookbook', 'Mr. Hide', NULL, true);
    COMMIT;
    ```
    
    *Результат:*
    ```
    workshop=# INSERT INTO t_books (book_id, title, author, category, is_active)
        VALUES (150001, 'Cookbook', 'Mr. Hide', NULL, true);
        COMMIT;
    INSERT 0 1
    WARNING:  there is no transaction in progress
    COMMIT
    ```

21. Создайте индекс по категории:
    ```sql
    CREATE INDEX t_books_cat_idx ON t_books(category);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX t_books_cat_idx ON t_books(category);
    CREATE INDEX
    ```

22. Найдите книги без категории:
    ```sql
    EXPLAIN ANALYZE
    SELECT author, title 
    FROM t_books 
    WHERE category IS NULL;
    ```
    
    *План выполнения:*
    ```
     Index Scan using t_books_cat_idx on t_books  (cost=0.29..8.15 rows=1 width=21) (actual time=0.029..0.030 rows=1 loops=1)
       Index Cond: (category IS NULL)
     Planning Time: 0.234 ms
     Execution Time: 0.043 ms
    (4 rows)
    ```
    
    *Объясните результат:*
    
    `NULL` значения тоже индексируются, так что PostgreSQL использует созданный индекс `t_books_cat_idx` по колонке `category` для поиска таких значений.

23. Создайте частичные индексы:
    ```sql
    DROP INDEX t_books_cat_idx;
    CREATE INDEX t_books_cat_null_idx ON t_books(category) WHERE category IS NULL;
    ```
    
    *Результат:*
    ```
    workshop=# DROP INDEX t_books_cat_idx;
        CREATE INDEX t_books_cat_null_idx ON t_books(category) WHERE category IS NULL;
    DROP INDEX
    CREATE INDEX
    ```

24. Повторите запрос из шага 22:
    ```sql
    EXPLAIN ANALYZE
    SELECT author, title 
    FROM t_books 
    WHERE category IS NULL;
    ```
    
    *План выполнения:*
    ```
     Index Scan using t_books_cat_null_idx on t_books  (cost=0.12..7.98 rows=1 width=21) (actual time=0.033..0.034 rows=1 loops=1)
     Planning Time: 0.186 ms
     Execution Time: 0.044 ms
    (3 rows)
    ```
    
    *Объясните результат:*
    
    PostgreSQL использовал созданный индекс с методом `Index Scan`, поскольку индекс как раз содержит информацию по строкам с `category IS NULL`. 

25. Создайте частичный уникальный индекс:
    ```sql
    CREATE UNIQUE INDEX t_books_selective_unique_idx 
    ON t_books(title) 
    WHERE category = 'Science';
    
    -- Протестируйте его
    INSERT INTO t_books (book_id, title, author, category, is_active)
    VALUES (150002, 'Unique Science Book', 'Author 1', 'Science', true);
    
    -- Попробуйте вставить дубликат
    INSERT INTO t_books (book_id, title, author, category, is_active)
    VALUES (150003, 'Unique Science Book', 'Author 2', 'Science', true);
    
    -- Но можно вставить такое же название для другой категории
    INSERT INTO t_books (book_id, title, author, category, is_active)
    VALUES (150004, 'Unique Science Book', 'Author 3', 'History', true);
    ```
    
    *Результат:*
    ```
    workshop=# CREATE UNIQUE INDEX t_books_selective_unique_idx 
        ON t_books(title) 
        WHERE category = 'Science';
    CREATE INDEX
    ```
    ```
    workshop=# INSERT INTO t_books (book_id, title, author, category, is_active)
        VALUES (150002, 'Unique Science Book', 'Author 1', 'Science', true);
    INSERT 0 1
    ```
    ```
    workshop=# INSERT INTO t_books (book_id, title, author, category, is_active)
        VALUES (150003, 'Unique Science Book', 'Author 2', 'Science', true);
    ERROR:  duplicate key value violates unique constraint "t_books_selective_unique_idx"
    DETAIL:  Key (title)=(Unique Science Book) already exists.
    ```
    ```
    workshop=# INSERT INTO t_books (book_id, title, author, category, is_active)
        VALUES (150004, 'Unique Science Book', 'Author 3', 'History', true);
    INSERT 0 1
    ```
    
    *Объясните результат:*
    
    Этот индекс будет использован только при вставке строки с `category = 'Science'` и будет проверять, что существует не более одной строки с такой категорией. Именно поэтому вторая вставка завершилась ошибкой, а первая (создающая первую строку с `category = 'Science'`) и третья (где `category` не `'Science'`) успешно выполнились.