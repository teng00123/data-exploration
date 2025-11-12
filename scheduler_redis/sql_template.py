class SqlTemplate:


    constrain_query = """
                        SELECT acc.column_name
                        FROM all_constraints ac
                        JOIN all_cons_columns acc ON ac.constraint_name = acc.constraint_name
                        WHERE ac.constraint_type = 'P'
                        AND ac.table_name = '{table_name}'
                        """
    columns_query = """
                        SELECT utc.column_name,
                        utc.data_type,
                        utc.data_length,
                        utc.data_precision,
                        utc.data_scale,
                        utc.nullable,
                        ucc.comments AS column_comment
                        FROM   all_tab_columns utc
                        JOIN   all_col_comments ucc
                        ON     utc.table_name = ucc.table_name
                        AND    utc.column_name = ucc.column_name
                        WHERE  utc.table_name = '{table_name}'
                        """
    table_comment_query = """
                        SELECT table_name, comments
                        FROM all_tab_comments
                        WHERE table_name = '{table_name}'
                        AND owner = '{schema_name}'
                        """

    table_datastorge_query = """
                        select bytes/1024/1024 as sizes from dba_segments where 
                       segment_type='TABLE' and owner='{schema_name}' and segment_name='{table_name}' """
