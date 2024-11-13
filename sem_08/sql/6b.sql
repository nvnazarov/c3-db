SELECT min_salary, max_salary FROM jobs WHERE job_id = 'SY_ANAL';
SELECT employee_id, last_name, salary FROM employees WHERE job_id = 'SY_ANAL';
CALL upd_jobsal('SY_ANAL', 5000, 7000);
CALL upd_jobsal('SY_ANAL', 7000, 18000);