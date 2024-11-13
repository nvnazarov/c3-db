CREATE OR REPLACE FUNCTION check_sal_range_func() 
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_employee RECORD;
BEGIN
    FOR v_employee IN 
        SELECT *
        FROM employees
        WHERE job_id = NEW.job_id
    LOOP
        IF v_employee.salary < NEW.min_salary OR v_employee.salary > NEW.max_salary
        THEN
            RAISE EXCEPTION 
                'Employee % salary % is out of the new salary range for job with job_id = %.',
                v_employee.employee_id, v_employee.salary, NEW.job_id;
        END IF;
    END LOOP;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER check_sal_range
BEFORE UPDATE OF min_salary, max_salary ON jobs
FOR EACH ROW
EXECUTE FUNCTION check_sal_range_func();