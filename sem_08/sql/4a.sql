CREATE OR REPLACE FUNCTION get_years_service(p_employee_id INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_years_service INTEGER;
BEGIN
    SELECT EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) INTO v_years_service
    FROM employees
    WHERE employee_id = p_employee_id;

    IF v_years_service IS NULL THEN
        RAISE EXCEPTION 'Employee with id = % not found.', p_employee_id;
    END IF;

    RETURN v_years_service;
END;
$$;