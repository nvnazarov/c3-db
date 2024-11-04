# ДЗ 7

1. Запустите БД в контейнере Docker.

    ```sh
    docker compose up -d
    ```

2. Запустите миграции:
    - Первая создает все таблицы;
    - Вторая и третья заполняют таблицы `countries` и `olympics` данными.

    `alembic` - инструмент для создания миграций от разработчиков `sqlalchemy` - ORM для Python.

    ```sh
    alembic upgrade head 
    ```

3. Запустите скрипт `seeder.py`, который заполнит БД фейковыми данными.

    ```sh
    py seeder.py       # Windows
    python3 seeder.py  # Linux
    ```

    Можно указать дополнительные параметры при запуске скрипта, чтобы их посмотреть, можно использовать флаг `-h`:

    ```sh
    py seeder.py -h       # Windows
    python3 seeder.py -h  # Linux
    ```

4. Запустите скрипт `tasks.py`, который выполнит запросы из задания.

    ```sh
    py tasks.py       # Windows
    python3 tasks.py  # Linux
    ```

    Результат выполнения запросов:
    
    ```sh
    ### QUERY 1 ###
    [(Decimal('1964'), 2, 2),
     (Decimal('1966'), 1, 1),
     (Decimal('1967'), 2, 5),
     (Decimal('1968'), 2, 2),
     (Decimal('1969'), 1, 2),
     (Decimal('1970'), 1, 1),
     (Decimal('1973'), 2, 2),
     (Decimal('1974'), 1, 1),
     (Decimal('1978'), 1, 1),
     (Decimal('1979'), 1, 1),
     (Decimal('1981'), 1, 1),
     (Decimal('1983'), 1, 1),
     (Decimal('1984'), 1, 1),
     (Decimal('1985'), 2, 2),
     (Decimal('1986'), 2, 2),
     (Decimal('1988'), 1, 2),
     (Decimal('1991'), 1, 1),
     (Decimal('1992'), 1, 1),
     (Decimal('1994'), 2, 2),
     (Decimal('1995'), 2, 3),
     (Decimal('1996'), 2, 2),
     (Decimal('1998'), 1, 1),
     (Decimal('1999'), 1, 1),
     (Decimal('2000'), 2, 3),
     (Decimal('2001'), 1, 2),
     (Decimal('2002'), 4, 5),
     (Decimal('2004'), 1, 1),
     (Decimal('2005'), 1, 1),
     (Decimal('2008'), 2, 2)]

    ### QUERY 2 ###
    [('b1c7b0a', 'Long Jump Men'),
     ('81a261c', 'High Jump Women'),
     ('2663b06', '100m Backstroke Men'),
     ('b542050', '100m Backstroke Women'),
     ('041c8c8', 'High Jump Men'),
     ('dde0dc7', '100m Breaststroke Men'),
     ('33a66f6', '10000m Men'),
     ('6cdb29e', 'Shot Put Men'),
     ('8b070c3', 'Hammer Throw Men'),
     ('410ccac', '100m Breaststroke Men'),
     ('1e90c6d', '100m Backstroke Women'),
     ('c0a08f7', '100m Backstroke Men'),
     ('0aca378', '10000m Men')]

    ### QUERY 3 ###
    [('3944ea0041', 'SYD2000'), ('29f17d230e', 'SYD2000'), ('a88a3432da', 'SYD2000'), ('57f1311a03', 'SYD2000'),
     ('c7faaf09b2', 'SYD2000'), ('d0b86b19d9', 'SYD2000'), ('f4615ba5ac', 'ATH2004'), ('c65717c4fd', 'SYD2000'),
     ('7894df18ee', 'ATH2004'), ('7ddd5181ad', 'ATH2004'), ('d994872cb4', 'SYD2000'), ('fde6aff10c', 'SYD2000'),
     ('90f1a7cf44', 'ATH2004'), ('7f840882cc', 'SYD2000'), ('16ded0c91b', 'SYD2000'), ('d994872cb4', 'ATH2004'),
     ('fc68b1ecc9', 'ATH2004'), ('13e8a1ada5', 'SYD2000'), ('e5c715fed0', 'ATH2004'), ('fc6e04ec54', 'ATH2004'),
     ('f815a67cae', 'ATH2004'), ('9485443db4', 'ATH2004'), ('4e6461cbb9', 'SYD2000'), ('0af6d843c5', 'SYD2000'),
     ('ad7596ba1d', 'ATH2004'), ('d3b52da6a0', 'SYD2000'), ('135e64a092', 'ATH2004'), ('3a82a50a2b', 'ATH2004'),
     ('d2d9e75abd', 'ATH2004'), ('fde6aff10c', 'ATH2004'), ('113a41df62', 'SYD2000'), ('fa27a9d863', 'ATH2004'),
     ('7ddd5181ad', 'SYD2000'), ('3e9183b4d6', 'ATH2004'), ('c60f3cfd07', 'SYD2000'), ('c7faaf09b2', 'ATH2004'),
     ('2c9b05334a', 'SYD2000'), ('9e10444020', 'ATH2004'), ('86d71d9d03', 'SYD2000'), ('fc68b1ecc9', 'SYD2000'),
     ('a88a3432da', 'ATH2004'), ('a8567bcd8e', 'SYD2000'), ('0dbf771a5e', 'SYD2000'), ('c8f6ad74f9', 'SYD2000'),
     ('2d1c640508', 'ATH2004'), ('51eb5eeb76', 'ATH2004'), ('fcc87aa2de', 'SYD2000'), ('f815a67cae', 'SYD2000'),
     ('57f1311a03', 'ATH2004'), ('e7e0ea14ef', 'ATH2004'), ('29f17d230e', 'ATH2004'), ('3a82a50a2b', 'SYD2000'),
     ('fd8749adda', 'ATH2004'), ('044ee4dfd9', 'ATH2004'), ('259037a7e0', 'ATH2004'), ('a7a5d57919', 'ATH2004'),
     ('ee77da52bf', 'SYD2000'), ('e7e0ea14ef', 'SYD2000'), ('277d0a0ebe', 'SYD2000'), ('6adc4bf13d', 'SYD2000'),
     ('47445e591f', 'ATH2004'), ('070c03743a', 'SYD2000'), ('070c03743a', 'ATH2004'), ('86d71d9d03', 'ATH2004'),
     ('a32bf17092', 'SYD2000'), ('2c9b05334a', 'ATH2004'), ('7e38b33aa1', 'ATH2004'), ('e5c715fed0', 'SYD2000'),
     ('fcc87aa2de', 'ATH2004'), ('48e384d57e', 'ATH2004'), ('e357ba97cd', 'ATH2004'), ('9485443db4', 'SYD2000'),
     ('451a7f1ab1', 'SYD2000'), ('ad7596ba1d', 'SYD2000'), ('c8f6ad74f9', 'ATH2004'), ('16ded0c91b', 'ATH2004'),
     ('8d35377894', 'SYD2000'), ('044ee4dfd9', 'SYD2000'), ('e9f0544009', 'SYD2000'), ('fb6c20a8f7', 'SYD2000'),
     ('d2d9e75abd', 'SYD2000'), ('c0dff90c78', 'SYD2000'), ('4e6461cbb9', 'ATH2004'), ('21dad4d457', 'SYD2000'),
     ('f10a2af94f', 'ATH2004'), ('90f1a7cf44', 'SYD2000'), ('e73b13b9c6', 'SYD2000'), ('0af6d843c5', 'ATH2004'),
     ('259037a7e0', 'SYD2000'), ('577613db8f', 'SYD2000'), ('a8567bcd8e', 'ATH2004'), ('8a5b4f8c66', 'SYD2000'),
     ('9e10444020', 'SYD2000'), ('21dad4d457', 'ATH2004'), ('7894df18ee', 'SYD2000'), ('6c2e496719', 'SYD2000'),
     ('3559c2ac5c', 'SYD2000'), ('8d35377894', 'ATH2004'), ('3e9183b4d6', 'SYD2000'), ('e357ba97cd', 'SYD2000'),
     ('7e38b33aa1', 'SYD2000'), ('d0b86b19d9', 'ATH2004'), ('479205d79d', 'ATH2004'), ('51eb5eeb76', 'SYD2000'),
     ('fb6c20a8f7', 'ATH2004'), ('0d476cbbef', 'ATH2004'), ('d357d6e87f', 'ATH2004'), ('fc6e04ec54', 'SYD2000'),
     ('479205d79d', 'SYD2000'), ('2d1c640508', 'SYD2000'), ('32acc4cb46', 'SYD2000'), ('a32bf17092', 'ATH2004'),
     ('48e384d57e', 'SYD2000'), ('4dc0ff397b', 'SYD2000'), ('6c2e496719', 'ATH2004'), ('6c853197c8', 'SYD2000'),
     ('113a41df62', 'ATH2004'), ('05b4f7d3ab', 'SYD2000'), ('e73b13b9c6', 'ATH2004'), ('3559c2ac5c', 'ATH2004'),
     ('c2f7a7a502', 'SYD2000'), ('3944ea0041', 'ATH2004'), ('a7a5d57919', 'SYD2000'), ('fd8749adda', 'SYD2000'),
     ('451a7f1ab1', 'ATH2004'), ('32acc4cb46', 'ATH2004'), ('ee77da52bf', 'ATH2004'), ('f10a2af94f', 'SYD2000'),
     ('49aa549f42', 'SYD2000'), ('d3b52da6a0', 'ATH2004'), ('8a5b4f8c66', 'ATH2004'), ('277d0a0ebe', 'ATH2004'),
     ('19d67122ef', 'ATH2004'), ('47445e591f', 'SYD2000'), ('ed98e83a87', 'SYD2000'), ('5c2eb497d7', 'ATH2004'),
     ('c65717c4fd', 'ATH2004'), ('ba3715751c', 'SYD2000'), ('d357d6e87f', 'SYD2000'), ('7f840882cc', 'ATH2004'),
     ('6adc4bf13d', 'ATH2004'), ('c2f7a7a502', 'ATH2004'), ('c0dff90c78', 'ATH2004'), ('0d476cbbef', 'SYD2000'),
     ('ba3715751c', 'ATH2004'), ('fa27a9d863', 'SYD2000'), ('c60f3cfd07', 'ATH2004'), ('13e8a1ada5', 'ATH2004'),
     ('3b5d369e9d', 'ATH2004'), ('bb6820a92c', 'ATH2004'), ('ed98e83a87', 'ATH2004'), ('6c853197c8', 'ATH2004'),
     ('05b4f7d3ab', 'ATH2004'), ('bb6820a92c', 'SYD2000'), ('135e64a092', 'SYD2000'), ('caf5e85e88', 'ATH2004'),
     ('caf5e85e88', 'SYD2000'), ('4dc0ff397b', 'ATH2004'), ('0dbf771a5e', 'ATH2004'), ('5c2eb497d7', 'SYD2000'),
     ('19d67122ef', 'SYD2000'), ('545b9692e9', 'ATH2004'), ('3b5d369e9d', 'SYD2000'), ('f4615ba5ac', 'SYD2000'),
     ('577613db8f', 'ATH2004'), ('49aa549f42', 'ATH2004'), ('545b9692e9', 'SYD2000'), ('e9f0544009', 'ATH2004')]

    ### QUERY 4 ###
    An error occured: (psycopg2.errors.UndefinedTable) missing FROM-clause entry for table "countries"

    ### QUERY 5 ###
    [('China                                   ', Decimal('3.0226913439187984197E-9')),
     ('Turkey                                  ', Decimal('1.4167063911138735E-8')),
     ('France                                  ', Decimal('1.6530144205672021E-8')),
     ('United States                           ', Decimal('3.6527860795643222E-8')),
     ('Russia                                  ', Decimal('4.1898973195830214E-8'))]
    ```