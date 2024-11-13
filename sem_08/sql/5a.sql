CREATE OR REPLACE FUNCTION get_job_count(p_employee_id INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_employee_count INTEGER;
    v_jobs_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_employee_count FROM employees WHERE employee_id = p_employee_id;
    IF v_employee_count = 0 THEN
        RAISE EXCEPTION 'Employee with id = % not found.', p_employee_id;
    END IF;

    SELECT COUNT(DISTINCT job_id) INTO v_jobs_count
    FROM (
        SELECT job_id
        FROM job_history
        WHERE employee_id = p_employee_id
        UNION
        SELECT job_id FROM employees WHERE employee_id = p_employee_id
    );

    RETURN v_jobs_count;
END;
$$;