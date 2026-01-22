BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
        job_name        => '"TARGET_SCHEMA"."JOB_PRC_LOAD_CTI_INDICATORS"',
        job_type        => 'STORED_PROCEDURE',
        job_action      => '"TARGET_SCHEMA"."PKG_SENTINEL_DATA_SYNC"."PRC_LOAD_CTI_INDICATORS"',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0',
        enabled         => TRUE,
        comments        => 'Daily sync for TEST_CTI_INDICATORS'
    );
END;
/