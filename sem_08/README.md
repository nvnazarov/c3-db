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

# 5

# 6