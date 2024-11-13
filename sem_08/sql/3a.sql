CREATE OR REPLACE PROCEDURE upd_jobsal(p_job_id VARCHAR(10), p_new_min_salary INTEGER, p_new_max_salary INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    v_job RECORD;
BEGIN
    IF p_new_max_salary < p_new_min_salary THEN
        RAISE EXCEPTION 'Max salary % is less than min salary %.', p_new_max_salary, p_new_min_salary;
    END IF;
    
    SELECT * INTO v_job FROM jobs WHERE job_id = p_job_id;
    IF v_job IS NULL THEN
        RAISE EXCEPTION 'Job with id = % not found.', p_job_id;
    END IF;

    UPDATE jobs
    SET
        min_salary = p_new_min_salary,
        max_salary = p_new_max_salary
    WHERE job_id = p_job_id;

    EXCEPTION
        WHEN SQLSTATE '55P03' THEN
            RAISE EXCEPTION 'The row in jobs table with job_id = % is locked.', p_job_id;
        WHEN OTHERS THEN
            RAISE;
END;
$$;