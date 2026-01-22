BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
        job_name        => '"TARGET_SCHEMA"."JOB_PRC_LOAD_HOME_GUARDIAN_CONFIG"',
        job_type        => 'STORED_PROCEDURE',
        job_action      => '"TARGET_SCHEMA"."PKG_SENTINEL_DATA_SYNC"."PRC_LOAD_HOME_GUARDIAN_CONFIG"',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0',
        enabled         => TRUE,
        comments        => 'Daily sync for TEST_HOME_GUARDIAN_CONFIG'
    );
END;
/