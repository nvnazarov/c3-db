# ДЗ 8

## Перед началом

Поднимаем сервис с БД:

```
docker compose up -d
```

Заходим в контейнер и запускаем `psql`:

```
PS C:\Users\Administrator\university\c3\db\sem_08> docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                    NAMES
7c0c5831e89e   postgres:alpine   "docker-entrypoint.s…"   4 seconds ago   Up 3 seconds   0.0.0.0:5438->5432/tcp   sem_08-db-jobs-1
PS C:\Users\Administrator\university\c3\db\sem_08> docker exec -it 7c bash
7c0c5831e89e:/# psql jobs superadmin
psql (17.0)
Type "help" for help.

jobs=#
```

## 1

a. Создаем процедуру `new_job` (см. `./sql/1a.sql`).

```
jobs=# CREATE OR REPLACE PROCEDURE new_job(p_job_id VARCHAR(10), p_job_title VARCHAR(35), p_min_salary INTEGER)
jobs-# LANGUAGE plpgsql
jobs-# AS $$
jobs$# BEGIN
jobs$#     INSERT INTO jobs(job_id, job_title, min_salary, max_salary)
jobs$#     VALUES (p_job_id, p_job_title, p_min_salary, p_min_salary * 2);
jobs$# END;
jobs$# $$
jobs-# ;
CREATE PROCEDURE
```

b. Пробуем вызвать процедуру (см. `./sql/1b.sql`).

```
jobs=# CALL new_job('SY_ANAL', 'System Analyst', 6000);
ERROR:  duplicate key value violates unique constraint "jobs_pkey"
DETAIL:  Key (job_id)=(SY_ANAL) already exists.
CONTEXT:  SQL statement "INSERT INTO jobs(job_id, job_title, min_salary, max_salary)
    VALUES (p_job_id, p_job_title, p_min_salary, p_min_salary * 2)"
PL/pgSQL function new_job(character varying,character varying,integer) line 3 at SQL statement
```

Как видим, ключ `SY_ANAL` уже присутствует в таблице `jobs`. Давайте попробуем вставить какую-то другую запись.

```
jobs=# CALL new_job('TEST_JOB', 'Test Job', 6000);
CALL
jobs=# SELECT * FROM jobs WHERE job_id = 'TEST_JOB';
  job_id  | job_title | min_salary | max_salary
----------+-----------+------------+------------
 TEST_JOB | Test Job  |       6000 |      12000
(1 row)
```

Все работает.

## 2

a. Создаем процедуру `add_job_hist` (см. `./sql/2a.sql`).

```
jobs=# CREATE OR REPLACE PROCEDURE add_job_hist(p_employee_id INTEGER, p_new_job_id VARCHAR(10))
jobs-# LANGUAGE plpgsql
jobs-# AS $$
jobs$# DECLARE
jobs$#     v_employee RECORD;
jobs$#     v_new_job RECORD;
jobs$# BEGIN
jobs$#     SELECT * INTO v_employee FROM employees WHERE employee_id = p_employee_id;
jobs$#     IF v_employee IS NULL THEN
jobs$#         RAISE EXCEPTION 'Employee with id = % not found.', p_employee_id;
jobs$#     END IF;
jobs$# 
jobs$#     SELECT * INTO v_new_job FROM jobs WHERE job_id = p_new_job_id;
jobs$#     IF v_new_job IS NULL THEN
jobs$#         RAISE EXCEPTION 'Job with id = % not found.', p_new_job_id;
jobs$#     END IF;
jobs$#
jobs$#     INSERT INTO job_history(employee_id, start_date, end_date, job_id, department_id)
jobs$#     VALUES (p_employee_id, v_employee.hire_date, CURRENT_DATE, v_employee.job_id, v_employee.department_id);
jobs$#
jobs$#     UPDATE employees
jobs$#     SET
jobs$#         hire_date = CURRENT_DATE,
jobs$#         job_id = p_new_job_id,
jobs$#         salary = v_new_job.min_salary + 500
jobs$#     WHERE employee_id = p_employee_id;
jobs$# END;
jobs$# $$;
CREATE PROCEDURE
```

b. (см. `./sql/2b.sql`)

Выключаем все триггеры.

```
jobs=# ALTER TABLE employees DISABLE TRIGGER ALL;
ALTER TABLE
jobs=# ALTER TABLE jobs DISABLE TRIGGER ALL;
ALTER TABLE
jobs=# ALTER TABLE job_history DISABLE TRIGGER ALL;
ALTER TABLE
```

Вызываем процедуру.

```
jobs=# CALL add_job_hist(106, 'SY_ANAL');
CALL
```

Проверяем результат (все ок).

```
jobs=# SELECT * FROM job_history WHERE employee_id = 106;
 employee_id | start_date |  end_date  | job_id  | department_id
-------------+------------+------------+---------+---------------
         106 | 2000-01-01 | 2022-11-13 | IT_PROG |            60
         106 | 2022-12-15 | 2024-11-13 | SY_ANAL |            60
(2 rows)

jobs=# SELECT * FROM employees WHERE employee_id = 106;
 employee_id | first_name | last_name |  email   | phone_integer | hire_date  | job_id  | salary  | commission_pct | manager_id | department_id
-------------+------------+-----------+----------+---------------+------------+---------+---------+----------------+------------+---------------
         106 | Valli      | Pataballa | VPATABAL | 590.423.4560  | 2024-11-13 | SY_ANAL | 6500.00 |                |        103 |            60
(1 row)
```

Возвращаем триггеры.

```
jobs=# ALTER TABLE employees ENABLE TRIGGER ALL;
ALTER TABLE
jobs=# ALTER TABLE jobs ENABLE TRIGGER ALL;
ALTER TABLE
jobs=# ALTER TABLE job_history ENABLE TRIGGER ALL;
ALTER TABLE
```

## 3

a. Создаем процедуру (см. `./sql/3a.sql`).

```
jobs=# CREATE OR REPLACE PROCEDURE upd_jobsal(p_job_id VARCHAR(10), p_new_min_salary INTEGER, p_new_max_salary INTEGER)
jobs-# LANGUAGE plpgsql
jobs-# AS $$
jobs$# DECLARE
jobs$#     v_job RECORD;
jobs$# BEGIN
jobs$#     IF p_new_max_salary < p_new_min_salary THEN
jobs$#         RAISE EXCEPTION 'Max salary % is less than min salary %.', p_new_max_salary, p_new_min_salary;
jobs$#     END IF;
jobs$#     
jobs$#     SELECT * INTO v_job FROM jobs WHERE job_id = p_job_id;
jobs$#     IF v_job IS NULL THEN
jobs$#         RAISE EXCEPTION 'Job with id = % not found.', p_job_id;
jobs$#     END IF;
jobs$# 
jobs$#     UPDATE jobs
jobs$#     SET
jobs$#         min_salary = p_new_min_salary,
jobs$#         max_salary = p_new_max_salary
jobs$#     WHERE job_id = p_job_id;
jobs$#
jobs$#     EXCEPTION
jobs$#         WHEN SQLSTATE '55P03' THEN
jobs$#             RAISE EXCEPTION 'The row in jobs table with job_id = % is locked.', p_job_id;
jobs$#         WHEN OTHERS THEN
jobs$#             RAISE;
jobs$# END;
jobs$# $$;
CREATE PROCEDURE
```

b. Вызываем процедуру с `min_salary` > `max_salary` (см. `./sql/3b.sql`).

```
jobs=# CALL upd_jobsal('SY_ANAL', 7000, 140);
ERROR:  Max salary 140 is less than min salary 7000.
CONTEXT:  PL/pgSQL function upd_jobsal(character varying,integer,integer) line 6 at RAISE
```

c. Отключаем триггеры на таблицах `jobs` и `employees` (см. `./sql/3c.sql`).

```
jobs=# ALTER TABLE employees DISABLE TRIGGER ALL;
ALTER TABLE
jobs=# ALTER TABLE jobs DISABLE TRIGGER ALL;
ALTER TABLE
```

d,e. Вызываем процедуру с нормальными параметрами и проверяем результат (см. `./sql/3d.sql` и `./sql/3e.sql`).

```
jobs=# BEGIN;
BEGIN
jobs=*# CALL upd_jobsal('SY_ANAL', 7000, 14000);
CALL
jobs=*# SELECT * FROM jobs WHERE job_id = 'SY_ANAL';
 job_id  |    job_title    | min_salary | max_salary 
---------+-----------------+------------+------------
 SY_ANAL | Systems Analyst |       7000 |      14000
(1 row)

jobs=*# COMMIT;
COMMIT
```

e. Включаем триггеры (см. `./sql/3e.sql`).

```
jobs=# ALTER TABLE employees ENABLE TRIGGER ALL;
ALTER TABLE
jobs=# ALTER TABLE jobs ENABLE TRIGGER ALL;
ALTER TABLE
```

# 4

a. Создаем функцию (см. `./sql/4a.sql`).

```
jobs=# CREATE OR REPLACE FUNCTION get_years_service(p_employee_id INTEGER)
jobs-# RETURNS INTEGER
jobs-# LANGUAGE plpgsql
jobs-# AS $$
jobs$# DECLARE
jobs$#     v_years_service INTEGER;
jobs$# BEGIN
jobs$#     SELECT EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) INTO v_years_service
jobs$#     FROM employees
jobs$#     WHERE employee_id = p_employee_id;
jobs$# 
jobs$#     IF v_years_service IS NULL THEN
jobs$#         RAISE EXCEPTION 'Employee with id = % not found.', p_employee_id;
jobs$#     END IF;
jobs$# 
jobs$#     RETURN v_years_service;
jobs$# END;
jobs$# $$;
CREATE FUNCTION
```

b. Вызываем функцию с некорректным работником (см. `./sql/4b.sql`).

```
jobs=# SELECT get_years_service(999);
ERROR:  Employee with id = 999 not found.
CONTEXT:  PL/pgSQL function get_years_service(integer) line 10 at RAISE
```

c. Вызываем функцию с корректными данными (см. `./sql/4c.sql`).

```
jobs=# SELECT get_years_service(106);
 get_years_service 
-------------------
                 0
(1 row)
```

d. Проверяем результат, все ок (см. `./sql/4d.sql`).

```
jobs=# SELECT * FROM employees WHERE employee_id = 106;
 employee_id | first_name | last_name |  email   | phone_integer | hire_date  | job_id  | salary  | commission_pct | manager_id | department_id
-------------+------------+-----------+----------+---------------+------------+---------+---------+----------------+------------+---------------
         106 | Valli      | Pataballa | VPATABAL | 590.423.4560  | 2024-11-13 | SY_ANAL | 6500.00 |                |        103 |            60
(1 row)

jobs=# SELECT * FROM job_history WHERE employee_id = 106;
 employee_id | start_date |  end_date  | job_id  | department_id
-------------+------------+------------+---------+---------------
         106 | 2000-01-01 | 2022-11-13 | IT_PROG |            60
         106 | 2022-12-15 | 2024-11-13 | SY_ANAL |            60
(2 rows)
```

# 5

a. Создаем функцию (см. `./sql/5a.sql`).

```
jobs=# CREATE OR REPLACE FUNCTION get_job_count(p_employee_id INTEGER)
jobs-# RETURNS INTEGER
jobs-# LANGUAGE plpgsql
jobs-# AS $$
jobs$# DECLARE
jobs$#     v_employee_count INTEGER;
jobs$#     v_jobs_count INTEGER;
jobs$# BEGIN
jobs$#     SELECT COUNT(*) INTO v_employee_count FROM employees WHERE employee_id = p_employee_id;
jobs$#     IF v_employee_count = 0 THEN
jobs$#         RAISE EXCEPTION 'Employee with id = % not found.', p_employee_id;
jobs$#     END IF;
jobs$# 
jobs$#     SELECT COUNT(DISTINCT job_id) INTO v_jobs_count
jobs$#     FROM (
jobs$#         SELECT job_id
jobs$#         FROM job_history
jobs$#         WHERE employee_id = p_employee_id
jobs$#         UNION
jobs$#         SELECT job_id FROM employees WHERE employee_id = p_employee_id
jobs$#     );
jobs$#
jobs$#     RETURN v_jobs_count;
jobs$# END;
jobs$# $$;
CREATE FUNCTION
```

b. Вызываем функцию (см. `./sql/5b.sql`).

```
jobs=# SELECT * FROM get_job_count(176);
 get_job_count
---------------
             2
(1 row)
```

# 6

a. Создаем триггер (см. `./sql/6a.sql`).

```
jobs=# CREATE OR REPLACE TRIGGER check_sal_range
jobs-# BEFORE UPDATE OF min_salary, max_salary ON jobs
jobs-# FOR EACH ROW
jobs-# EXECUTE FUNCTION check_sal_range_func();
jobs=# CREATE OR REPLACE FUNCTION check_sal_range_func() 
jobs-# RETURNS TRIGGER
jobs-# LANGUAGE plpgsql
jobs-# AS $$
jobs$# DECLARE
jobs$#     v_employee RECORD;
jobs$# BEGIN
jobs$#     FOR v_employee IN 
jobs$#         SELECT *
jobs$#         FROM employees
jobs$#         WHERE job_id = NEW.job_id
jobs$#     LOOP
jobs$#         IF v_employee.salary < NEW.min_salary OR v_employee.salary > NEW.max_salary
jobs$#         THEN
jobs$#             RAISE EXCEPTION 
jobs$#                 'Employee % salary % is out of the new salary range for job with job_id = %.',
jobs$#                 v_employee.employee_id, v_employee.salary, NEW.job_id;
jobs$#         END IF;
jobs$#     END LOOP;
jobs$# 
jobs$#     RETURN NEW;
jobs$# END;
jobs$# $$;
CREATE FUNCTION
jobs=# 
jobs=# CREATE OR REPLACE TRIGGER check_sal_range
jobs-# BEFORE UPDATE OF min_salary, max_salary ON jobs
jobs-# FOR EACH ROW
jobs-# EXECUTE FUNCTION check_sal_range_func();
CREATE TRIGGER
```

b. Проверяем работу триггера (см. `./sql/b.sql`).

Выводим текущий разброс зарплаты и реальную зарплату для `job_id` = `SY_ANAL`.
```
jobs=# SELECT min_salary, max_salary FROM jobs WHERE job_id = 'SY_ANAL';
 min_salary | max_salary 
------------+------------
       7000 |      14000
(1 row)

jobs=# SELECT employee_id, last_name, salary FROM employees WHERE job_id = 'SY_ANAL';
 employee_id | last_name | salary  
-------------+-----------+---------
         106 | Pataballa | 6500.00
(1 row)
```

Меняем мин. и макс. зарплату на 5000 и 7000, все ок.

```
jobs=# CALL upd_jobsal('SY_ANAL', 5000, 7000);
CALL
jobs=# SELECT * FROM jobs WHERE job_id = 'SY_ANAL';
 job_id  |    job_title    | min_salary | max_salary 
---------+-----------------+------------+------------
 SY_ANAL | Systems Analyst |       5000 |       7000
(1 row)
```

с. Пытаемся обновить зарплату так, чтобы у рабочего 106 зарплата вышла за границы.

```
jobs=# CALL upd_jobsal('SY_ANAL', 7000, 18000);
ERROR:  Employee 106 salary 6500.00 is out of the new salary range for job with job_id = SY_ANAL.
CONTEXT:  PL/pgSQL function check_sal_range_func() line 12 at RAISE
SQL statement "UPDATE jobs
    SET
        min_salary = p_new_min_salary,
        max_salary = p_new_max_salary
    WHERE job_id = p_job_id"
PL/pgSQL function upd_jobsal(character varying,integer,integer) line 14 at SQL statement
```

Как видим, триггер сработал правильно.