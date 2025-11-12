import time
import json
import dmPython
from sqlalchemy import create_engine,text
import urllib.parse



def start(database_name,table_name):

    username = 'XXJ_FB_BF'
    password = 'root123456'
    database_address = '59.225.206.75'
    prot = '10022'
    conn = dmPython.connect(user=username, password=password, server=database_address, port=prot)
    cursor = conn.cursor()
    cursor.execute(
        f"select table_name, comments from dba_tab_comments where table_type='TABLE' and owner = '{database_name}'")
    tab_comments_list = cursor.fetchall()
    result_list = []
    for table_name,table_comment in tab_comments_list:
        sql = f"""
        SELECT count(1) FROM "{database_name}"."{table_name}"
        """
        cursor.execute(sql)
        data_total = cursor.fetchone()[0]
        cursor.execute(
        f"select a.COLUMN_NAME from DBA_CONSTRAINTS b,DBA_CONS_COLUMNS a where a.CONSTRAINT_NAME = b.CONSTRAINT_NAME AND b.CONSTRAINT_TYPE = 'P' AND  b.TABLE_NAME = '{table_name}' AND b.OWNER = f'{database_name}'")
        constraint_column = cursor.fetchone()
        if constraint_column:
            constraints_column = constraint_column[0]
        else:
            constraints_column = 'ID'
        cursor.execute(
            f"select table_name,column_name,data_type,data_length,data_precision,data_scale, nullable,column_id from dba_tab_columns where table_name='{table_name}'")
        column_list = cursor.fetchall()

        cursor.execute(
            f"select table_name,column_name,comments from dba_col_comments where table_name='{table_name}'")
        comments_list = cursor.fetchall()
        merged_info = []
        for field in column_list:
            for comment in comments_list:
                if field[0] == comment[0] and field[1] == comment[1]:
                    merged_info.append(field + (comment[2],))
        columns = ['table_name', 'name', 'data_type', 'data_length', 'data_precision', 'data_scale',
                   'nullable', 'column_id', 'comments']
        columns_list = [dict(zip(columns, merged)) for merged in merged_info]
        for dict_columns in columns_list:
            dict_columns['data_length'] = int(dict_columns['data_length'])
            # dict_columns['data_scale'] = int(dict_columns['data_scale'])
            dict_columns['column_id'] = int(dict_columns['column_id'])
        table_dict = {
            "table_name": table_name,
            "table_comment": table_comment,
            "data_total": data_total,
            "constraints_column": constraints_column,
            "column_list": columns_list
        }
        result_list.append(table_dict)
    username= 'sjpc001'
    password = urllib.parse.quote_plus('sjpc@1&yjt!SJ')
    database_address = '59.225.206.73'
    prot = 14106
    database_name = 'sxfjyzd_sjpc_result_table_database'
    db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
    engine = create_engine(db_url)
    connection = engine.connect()
    sql = """
    INSERT INTO xbxfjdglxt_result_table (tableEName, tableCName, dataItemCName,dataItemEName,dataItemType,dataItemLength,dataItemKey,dataItemEmpty,dBNumber) VALUES 
    ({tableEName}, {tableCName}, {dataItemCName}, {dataItemEName}, {dataItemType}, {dataItemLength}, {dataItemKey}, {dataItemEmpty}, {dBNumber})
    
    """
    error_list = []
    for result_data in result_list:
        for data in result_data['column_list']:
            insert_sql = sql.format(
                tableEName="'" + result_data.get('table_name') + "'",
                tableCName="'" + result_data.get('table_comment') + "'"if result_data.get('table_comment') is not None else 'Null',
                dataItemCName="'" + data.get('comments') + "'" if data.get('comments') is not None else 'Null',
                dataItemEName="'" + data.get('name') + "'",
                dataItemType="'" + data.get('data_type') + "'",
                dataItemLength="'" + str(data.get('data_length')) + "'",
                dataItemKey="'" + '否' + "'",
                dataItemEmpty="'" + '是'+ "'" if data.get('nullable') == 'Y' else "'" + '否' + "'",
                dBNumber=result_data.get('data_total')
            )
            table_sql = f"""
            SELECT * FROM `xbxfjdglxt_result_table` where dataItemEName='{data.get('name')}' and tableEName='{result_data.get('table_name')}';
            """
            table_field = connection.execute(text(table_sql)).fetchall()
            if len(table_field) > 0:
                continue
            print(insert_sql)
            try:
                connection.execute(text(insert_sql))
                connection.commit()
            except Exception as e:
                error_list.append(insert_sql)
    print('--------ok--------------')
    for i in error_list:
        with open(f'error{table_name}.txt', 'a') as f:
            f.write(i + '\n')

if __name__ == '__main__':
    # 优待抚恤数据库
    start('XXJ_FB','xbxfjdglxt_result_table')
    # 褒扬纪念信息管理数据库
    # start('TYJR_SC_MARTYMEFACI','tyjrzhfwglpt_byjnxxgl_result_table')
    # # 电子档案数据库53分库
    # start('JDLK_D1_PROD_BQ','tyjrzhfwglpt_dzda53_result_table')
    # # 政务报送 UMC数据库
    # start('TYJR_SC_GOVAFFATRANS_UMC','tyjrzhfwglpt_zwbs_umc_result_table')
    # # 就业创业数据库
    # start('TYJR_SC_EMPLENTREP','tyjrzhfwglpt_jycy_result_table')
    # # 服务管理平台数据库
    # start('TYJR_SC_ONESTOPSERVICE','tyjrzhfwglpt_fwglpt_result_table')
    # # 电子档案数据库59分库
    # start('JDLK_D2_PROD_BQ','tyjrzhfwglpt_dzda59_result_table')
    # # 英烈纪念数据库
    # start('TYJR_SC_MARTYMEMO','tyjrzhfwglpt_yljnpt_result_table')
    # # 政策法规数据库
    # start('TYJR_POLICYLAW','tyjrzhfwglpt_zcfgpt_result_table')