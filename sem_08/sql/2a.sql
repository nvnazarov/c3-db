CREATE OR REPLACE PROCEDURE add_job_hist(p_employee_id INTEGER, p_new_job_id VARCHAR(10))
LANGUAGE plpgsql
AS $$
DECLARE
    v_employee RECORD;
    v_new_job RECORD;
BEGIN
    SELECT * INTO v_employee FROM employees WHERE employee_id = p_employee_id;
    IF v_employee IS NULL THEN
        RAISE EXCEPTION 'Employee with id = % not found.', p_employee_id;
    END IF;

    SELECT * INTO v_new_job FROM jobs WHERE job_id = p_new_job_id;
    IF v_new_job IS NULL THEN
        RAISE EXCEPTION 'Job with id = % not found.', p_new_job_id;
    END IF;

    INSERT INTO job_history(employee_id, start_date, end_date, job_id, department_id)
    VALUES (p_employee_id, v_employee.hire_date, CURRENT_DATE, v_employee.job_id, v_employee.department_id);
    
    UPDATE employees
    SET
        hire_date = CURRENT_DATE,
        job_id = p_new_job_id,
        salary = v_new_job.min_salary + 500
    WHERE employee_id = p_employee_id;
END;
$$