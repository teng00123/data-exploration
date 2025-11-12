class SQLTemplate:
    EMPTY_VALUE_DETECTION = """
    
    SELECT COUNT(1) FROM 
    {table_name}
    WHERE {field_name} IS NOT NULL OR {field_name} != '';
    
    """


    REPETITIVE_DETECTION = """
    
    SELECT {field_name}, COUNT(*)
    FROM {table_name}
    GROUP BY {field_name}
    HAVING COUNT(*) > 1;
    
    """

    TIMELINESS_DETECTION = """
    
    SELECT {field_name} FROM 
    {table_name}
    WHERE {field_name} is NOT NULL
    ORDER BY {field_name} DESC
    LIMIT 1
    ;
    
    """

    COUNT_SQL="""

    SELECT COUNT(1) FROM {table_name};

    """

    TIMELINESS_SQL_DAY = """
        SELECT {field_name}
    FROM {table_name}
    ORDER BY {field_name} DESC
    LIMIT 1
    """

    DETECTION_TIMELINESS_SQL = """
    SELECT {field_name}
    FROM {table_name}
    WHERE {field_name} BETWEEN '{before_time}' AND '{after_time}'
    ORDER BY {field_name} DESC
    LIMIT 1
    """


