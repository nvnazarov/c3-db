# Задание 1. B-tree индексы в PostgreSQL

1. Запустите БД через docker compose в ./src/docker-compose.yml:

2. Выполните запрос для поиска книги с названием 'Oracle Core' и получите план выполнения:

    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title = 'Oracle Core';
    ```
   
    *План выполнения:*
    ```
     Seq Scan on t_books  (cost=0.00..3100.00 rows=1 width=33) (actual time=15.580..15.580 rows=1 loops=1)
       Filter: ((title)::text = 'Oracle Core'::text)
       Rows Removed by Filter: 149999
     Planning Time: 0.311 ms
     Execution Time: 15.607 ms
    (5 rows)
    ```
   
   *Объясните результат:*

   Поскольку в таблице `t_books` нет индекса по колонке `title`, а оператор `WHERE` фильтрует именно по этой колонке, приходится обходить все строки с помощью `Seq Scan`. Как видно, `Planning Time` намного меньше `Execution Time`, поскольку он (видимо) ожидал использование индекса.

3. Создайте B-tree индексы:
    ```sql
    CREATE INDEX t_books_title_idx ON t_books(title);
    CREATE INDEX t_books_active_idx ON t_books(is_active);
    ```
   
    *Результат:*
    ```
    workshop=# CREATE INDEX t_books_title_idx ON t_books(title);
       CREATE INDEX t_books_active_idx ON t_books(is_active);
    CREATE INDEX
    CREATE INDEX
    ```

4. Проверьте информацию о созданных индексах:
    ```sql
    SELECT schemaname, tablename, indexname, indexdef
    FROM pg_catalog.pg_indexes
    WHERE tablename = 't_books';
    ```
   
    *Результат:*
    ```
     schemaname | tablename |     indexname      |                                 indexdef
    ------------+-----------+--------------------+---------------------------------------------------------------------------
     public     | t_books   | t_books_id_pk      | CREATE UNIQUE INDEX t_books_id_pk ON public.t_books USING btree (book_id)
     public     | t_books   | t_books_title_idx  | CREATE INDEX t_books_title_idx ON public.t_books USING btree (title)
     public     | t_books   | t_books_active_idx | CREATE INDEX t_books_active_idx ON public.t_books USING btree (is_active)
    (3 rows)
    ```
   
   *Объясните результат:*
   
   Здесь есть индекс `t_books_id_pk`, который PostgreSQL создал самостоятельно, поскольку это индекс для колонки PK (он также помечен как `UNIQUE` чтобы не допустить добавление дубликатов PK). Также здесь есть два созданных нами индекса, они имеют тип `btree` (тип по умолчанию в PostgreSQL).

5. Обновите статистику таблицы:
    ```sql
    ANALYZE t_books;
    ```
   
    *Результат:*
   
    ```
    workshop=# ANALYZE t_books;
    ANALYZE
    ```

6. Выполните запрос для поиска книги 'Oracle Core' и получите план выполнения:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title = 'Oracle Core';
    ```
   
    *План выполнения:*
    ```
     Index Scan using t_books_title_idx on t_books  (cost=0.42..8.44 rows=1 width=33) (actual time=0.590..0.591 rows=1 loops=1)
       Index Cond: ((title)::text = 'Oracle Core'::text)
     Planning Time: 0.749 ms
     Execution Time: 0.605 ms
    (4 rows)
    ```
   
    *Объясните результат:*
    Используется `Index Scan`, поскольку в `WHERE` условие только на полное соответствие (`=`) колонки `title`, для которой мы создавали индекс. Также видно, что Planning Time и Execution Time стали примерно равны - признак того, что запрос хорошо оптимизирован.

7. Выполните запрос для поиска книги по book_id и получите план выполнения:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE book_id = 18;
    ```
   
    *План выполнения:*
    ```
     Index Scan using t_books_id_pk on t_books  (cost=0.42..8.44 rows=1 width=33) (actual time=0.672..0.673 rows=1 loops=1)
       Index Cond: (book_id = 18)
     Planning Time: 0.067 ms
     Execution Time: 0.687 ms
    (4 rows)
    ```
   
   *Объясните результат:*
   
    Аналогично, используется индекс, созданный PostgreSQL для PK таблицы `t_books`.

8. Выполните запрос для поиска активных книг и получите план выполнения:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE is_active = true;
    ```
   
    *План выполнения:*
    ```
     Seq Scan on t_books  (cost=0.00..2725.00 rows=75000 width=33) (actual time=0.008..9.740 rows=74680 loops=1)
       Filter: is_active
       Rows Removed by Filter: 75320
     Planning Time: 0.075 ms
     Execution Time: 11.537 ms
    (5 rows)
    ```
    
    *Объясните результат:*
    
    Несмотря на то, что есть индекс по столбцу `is_active`, он не используется, поскольку столбец содержит только 2 значения (`true` и `false`). В таком случае индекс не дает ожидаемого преимущества (особенно если классы сбалансированы).
    
9. Посчитайте количество строк и уникальных значений:
    ```sql
    SELECT
        COUNT(*) as total_rows,
        COUNT(DISTINCT title) as unique_titles,
        COUNT(DISTINCT category) as unique_categories,
        COUNT(DISTINCT author) as unique_authors
    FROM t_books;
    ```
   
    *Результат:*
    ```
     total_rows | unique_titles | unique_categories | unique_authors 
    ------------+---------------+-------------------+----------------
         150000 |        150000 |                 6 |           1003
    (1 row)
    ```

10. Удалите созданные индексы:
    ```sql
    DROP INDEX t_books_title_idx;
    DROP INDEX t_books_active_idx;
    ```
    
    *Результат:*
    ```
    workshop=# DROP INDEX t_books_title_idx;
        DROP INDEX t_books_active_idx;
    DROP INDEX
    DROP INDEX
    ```

11. Основываясь на предыдущих результатах, создайте индексы для оптимизации следующих запросов:
    a. `WHERE title = $1 AND category = $2`
    b. `WHERE title = $1`
    c. `WHERE category = $1 AND author = $2`
    d. `WHERE author = $1 AND book_id = $2`
    
    *Созданные индексы:*
    ```
    workshop=# CREATE INDEX t_books_title_category_idx ON t_books(title, category);
    CREATE INDEX
    workshop=# CREATE INDEX t_books_author_category_idx ON t_books(author, category);
    CREATE INDEX
    ```
    
    *Объясните ваше решение:*
    
    Для оптимизации запросов (a) и (b) можно создать один индекс по столбцам `title` и `category` (именно в таком порядке). Такой индекс эффективен для поиска точных сравнений как по столбцу `title`, так и по паре столбцов (`title`, `category`). Аналогично, для оптимизации запросов (c) и (d) можно создать индекс по столбцам `author` и `category` (в таком порядке). Единственное отличие в том, что в запросе (d) будет (скорее всего) использоваться индекс по PK таблицы `t_books`, поскольку может существовать только одна строка с `book_id = $2`.

12. Протестируйте созданные индексы.

    *Результаты тестов:*
    ```
    workshop=# EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title = 'Oracle Core' AND category = 'Science';
                                                                 QUERY PLAN
    -------------------------------------------------------------------------------------------------------------------------------------
     Index Scan using t_books_title_category_idx on t_books  (cost=0.42..8.44 rows=1 width=33) (actual time=0.049..0.049 rows=0 loops=1)
       Index Cond: (((title)::text = 'Oracle Core'::text) AND ((category)::text = 'Science'::text))
     Planning Time: 0.082 ms
     Execution Time: 0.062 ms
    (4 rows)
    ```

    ```
    workshop=# EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title = 'Oracle Core';
                                                                 QUERY PLAN
    -------------------------------------------------------------------------------------------------------------------------------------
     Index Scan using t_books_title_category_idx on t_books  (cost=0.42..8.44 rows=1 width=33) (actual time=0.023..0.024 rows=1 loops=1)
       Index Cond: ((title)::text = 'Oracle Core'::text)
     Planning Time: 0.067 ms
     Execution Time: 0.037 ms
    (4 rows)
    ```

    ```
    workshop=# EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE category = 'Science' AND author = 'Author_538';
                                                                  QUERY PLAN
    --------------------------------------------------------------------------------------------------------------------------------------
     Bitmap Heap Scan on t_books  (cost=4.60..110.97 rows=30 width=33) (actual time=0.069..0.113 rows=34 loops=1)
       Recheck Cond: (((author)::text = 'Author_538'::text) AND ((category)::text = 'Science'::text))
       Heap Blocks: exact=32
       ->  Bitmap Index Scan on t_books_author_category_idx  (cost=0.00..4.59 rows=30 width=0) (actual time=0.061..0.061 rows=34 loops=1)
             Index Cond: (((author)::text = 'Author_538'::text) AND ((category)::text = 'Science'::text))
     Planning Time: 0.079 ms
     Execution Time: 0.132 ms
    (7 rows)
    ```

    ```
    workshop=# EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE author = 'Author_538' AND book_id = '8';
                                                           QUERY PLAN
    ------------------------------------------------------------------------------------------------------------------------
     Index Scan using t_books_id_pk on t_books  (cost=0.42..8.44 rows=1 width=33) (actual time=0.021..0.021 rows=0 loops=1)
       Index Cond: (book_id = 8)
       Filter: ((author)::text = 'Author_538'::text)
       Rows Removed by Filter: 1
     Planning Time: 0.070 ms
     Execution Time: 0.034 ms
    (6 rows)
    ```
    
    *Объясните результаты:*
    
    Все выполнилось так, как было описано в п. 11. Однако, для запроса (c) PostgreSQL использовал Bitmap Index Scan и Bitmap Heap Scan. Видимо, PostgreSQL решил, что этот метод будет эффективнее обычного Index Scan.

13. Выполните регистронезависимый поиск по началу названия:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title ILIKE 'Relational%';
    ```
    
    *План выполнения:*
    ```
     Seq Scan on t_books  (cost=0.00..3100.00 rows=15 width=33) (actual time=59.440..59.441 rows=0 loops=1)
       Filter: ((title)::text ~~* 'Relational%'::text)
       Rows Removed by Filter: 150000
     Planning Time: 2.105 ms
     Execution Time: 59.471 ms
    (5 rows)
    ```
    
    *Объясните результат:*

    Нельзя применить индекс, поскольку здесь соответствие по паттерну (то есть неизвестно, как выглядит ключ на самом деле).

14. Создайте функциональный индекс:
    ```sql
    CREATE INDEX t_books_up_title_idx ON t_books(UPPER(title));
    ```
    
    *Результат:*
    ```
    workshop=# CREATE INDEX t_books_up_title_idx ON t_books(UPPER(title));
    CREATE INDEX
    ```

15. Выполните запрос из шага 13 с использованием UPPER:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE UPPER(title) LIKE 'RELATIONAL%';
    ```
    
    *План выполнения:*
    
    ```
                                                   QUERY PLAN
    ---------------------------------------------------------------------------------------------------------
     Seq Scan on t_books  (cost=0.00..3475.00 rows=750 width=33) (actual time=33.823..33.824 rows=0 loops=1)
       Filter: (upper((title)::text) ~~ 'RELATIONAL%'::text)
       Rows Removed by Filter: 150000
     Planning Time: 0.186 ms
     Execution Time: 33.839 ms
    (5 rows)
    ```
    
    *Объясните результат:*
    
    Аналогично предыдущему пункту, индекс не применяется для проверки соответствия паттерну.

16. Выполните поиск подстроки:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title ILIKE '%Core%';
    ```
    
    *План выполнения:*
    ```
     Seq Scan on t_books  (cost=0.00..3100.00 rows=15 width=33) (actual time=56.325..56.328 rows=1 loops=1)
       Filter: ((title)::text ~~* '%Core%'::text)
       Rows Removed by Filter: 149999
     Planning Time: 0.204 ms
     Execution Time: 56.342 ms
    (5 rows)
    ```
    
    *Объясните результат:*
    
    Аналогично предыдущему пункту, индекс не применяется для проверки соответствия паттерну.

17. Попробуйте удалить все индексы:
    ```sql
    DO $$ 
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT indexname FROM pg_indexes 
                  WHERE tablename = 't_books' 
                  AND indexname != 'books_pkey')
        LOOP
            EXECUTE 'DROP INDEX ' || r.indexname;
        END LOOP;
    END $$;
    ```
    
    *Результат:*
    ```
    ERROR:  cannot drop index t_books_id_pk because constraint t_books_id_pk on table t_books requires it
    HINT:  You can drop constraint t_books_id_pk on table t_books instead.
    CONTEXT:  SQL statement "DROP INDEX t_books_id_pk"
    PL/pgSQL function inline_code_block line 9 at EXECUTE
    ```
    
    *Объясните результат:*
    
    Нельзя удалить индекс, который используется каким-то constraint. В нашем случае, индекс `t_books_id_pk` используется для поддержания условия уникальности PK в таблице `t_books`. Его использует constraint с таким же названием - `t_books_id_pk`.

18. Создайте индекс для оптимизации суффиксного поиска:
    ```sql
    -- Вариант 1: с reverse()
    CREATE INDEX t_books_rev_title_idx ON t_books(reverse(title));
    
    -- Вариант 2: с триграммами
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
    CREATE INDEX t_books_trgm_idx ON t_books USING gin (title gin_trgm_ops);
    ```
    
    *Результаты тестов:*
    ```
    workshop=# EXPLAIN ANALYZE
        SELECT * FROM t_books WHERE title LIKE '%Core';
                                                            QUERY PLAN
    ---------------------------------------------------------------------------------------------------------------------------
     Bitmap Heap Scan on t_books  (cost=30.25..85.46 rows=15 width=33) (actual time=0.030..0.031 rows=1 loops=1)
       Recheck Cond: ((title)::text ~~ '%Core'::text)
       Heap Blocks: exact=1
       ->  Bitmap Index Scan on t_books_trgm_idx  (cost=0.00..30.25 rows=15 width=0) (actual time=0.023..0.023 rows=1 loops=1)
             Index Cond: ((title)::text ~~ '%Core'::text)
     Planning Time: 0.348 ms
     Execution Time: 0.064 ms
    (7 rows)
    ```
    
    *Объясните результаты:*
    
    Здесь мы используем расширение PostgreSQL - модуль `pg_trgm`, предоставляющий поиск по триграммам. Из документации знаем, что индекс типа GIN поддерживает "trigram-based index searches for `LIKE`, `ILIKE`, `~`, `~*` and `=` queries". Поэтому этот индексс и был использован в плане запроса, в комбинации с Bitmap Index Scan.

19. Выполните поиск по точному совпадению:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title = 'Oracle Core';
    ```
    
    *План выполнения:*
    ```
     Index Scan using t_books_title_category_idx on t_books  (cost=0.42..8.44 rows=1 width=33) (actual time=0.012..0.013 rows=1 loops=1)
       Index Cond: ((title)::text = 'Oracle Core'::text)
     Planning Time: 0.171 ms
     Execution Time: 0.024 ms
    (4 rows)
    ```
    
    *Объясните результат:*
    
    Здесь ничего не поменялось, поскольку у нас все еще есть индекс по столбцу `title`.

20. Выполните поиск по началу названия:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books WHERE title ILIKE 'Relational%';
    ```
    
    *План выполнения:*
    ```
     Bitmap Heap Scan on t_books  (cost=95.15..150.36 rows=15 width=33) (actual time=0.038..0.039 rows=0 loops=1)
       Recheck Cond: ((title)::text ~~* 'Relational%'::text)
       Rows Removed by Index Recheck: 1
       Heap Blocks: exact=1
       ->  Bitmap Index Scan on t_books_trgm_idx  (cost=0.00..95.15 rows=15 width=0) (actual time=0.018..0.018 rows=1 loops=1)
             Index Cond: ((title)::text ~~* 'Relational%'::text)
     Planning Time: 0.135 ms
     Execution Time: 0.053 ms
    (8 rows)
    ```
    
    *Объясните результат:*

    Аналогично п. 18.

21. Создайте свой пример индекса с обратной сортировкой:
    ```sql
    CREATE INDEX t_books_desc_idx ON t_books(title DESC);
    ```
    
    *Тестовый запрос:*
    ```
    EXPLAIN ANALYZE
    SELECT * FROM t_books ORDER BY title DESC;
    ```
    
    *План выполнения:*
    ```
    workshop=# EXPLAIN ANALYZE
        SELECT * FROM t_books ORDER BY title DESC;
                                                                   QUERY PLAN
    -----------------------------------------------------------------------------------------------------------------------------------------
     Index Scan using t_books_desc_idx on t_books  (cost=0.42..9062.87 rows=150000 width=33) (actual time=0.056..23.208 rows=150000 loops=1)
     Planning Time: 0.286 ms
     Execution Time: 26.761 ms
    (3 rows)
    ```
    
    *Объясните результат:*
    
    Поскольку данные в индексе `t_books_desc_idx` сортированы в порядке убывания, то в запросе, где данные нужно сортировать по убыванию `title`, эффективно использовать этот индекс. 