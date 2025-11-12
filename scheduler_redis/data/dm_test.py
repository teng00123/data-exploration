import time
import json
import dmPython
from sqlalchemy import create_engine, text
import urllib.parse
from sqlalchemy.inspection import inspect



def start(name,table_name):
    username = 'DMDBA'
    password = 'SC_DMDBA123'
    database_address = '59.225.205.32'
    prot = '5237'
    database_name='DAMENG'
    conn = dmPython.connect(user=username, password=password, server=database_address, port=prot)
    cursor = conn.cursor()

    username = 'sjpc001'
    password = urllib.parse.quote_plus('sjpc@7&zwfwhzyjyzx!ZW')
    database_address = '59.225.206.73'
    prot = 14406
    result_table_name = 'ythfwpt_result_table'
    database_name = 'sjgswglj_sjpc_result_table_database'
    db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
    engine = create_engine(db_url)
    connection = engine.connect()
    sql = """
        INSERT INTO {table_name} (tableEName, tableCName, dataItemCName,dataItemEName,dataItemType,dataItemLength,dataItemKey,dataItemEmpty,dBNumber) VALUES 
        ({tableEName}, {tableCName}, {dataItemCName}, {dataItemEName}, {dataItemType}, {dataItemLength}, {dataItemKey}, {dataItemEmpty}, {dBNumber})

        """

    cursor.execute(
        f"select comments from dba_tab_comments where table_type='TABLE' and table_name='{table_name}' and owner ='{name}'")
    tab_comment = cursor.fetchone()[0]
    if tab_comment is None:
        tab_comment = ''
    cursor.execute(
        f"select count(1) from {name}.{table_name}")
    tab_count = cursor.fetchone()[0]
    cursor.execute(
        f"select table_name,column_name,data_type,data_length,data_precision,data_scale, nullable,column_id from dba_tab_columns where table_name='{table_name}' and owner='{name}'")
    column_list = cursor.fetchall()
    for tab_name,column_name,data_type,data_length,data_precision,data_scale, nullable,column_id in column_list:
        cursor.execute(
            f"select comments from dba_col_comments where table_name='{table_name}' and column_name='{column_name}'")
        comment = cursor.fetchone()[0]
        if comment is None:
            comment = ''
        nullable = '是' if nullable == 'Y' else '否'

        insert_sql = sql.format(
            table_name=result_table_name,
            tableEName="'" + table_name + "'",
            tableCName="'" + tab_comment + "'" ,
            dataItemCName="'" + comment + "'" ,
            dataItemEName="'" + column_name + "'",
            dataItemType="'" + data_type + "'",
            dataItemLength="'" + str(data_length) + "'",
            dataItemKey="'" + '否' + "'",
            dataItemEmpty="'" + nullable + "'",
            dBNumber=tab_count
        )
        connection.execute(text(insert_sql))
        connection.commit()


if __name__ == '__main__':
    # 机关服务系统
    start('JGFWXT','JGSWJ_MANAGEMENT_APPOINTMENT')
    start('JGFWXT','JGSWJ_TAKEAWAY_RECORD')
    #
    # # 文档资源管理共享系统
    start('SPIDERELEC','EAM_ARCHIVE_CONTENT')
    start('SPIDERELEC','EAM_ARCHIVE_FILE')
    start('SPIDERELEC','EAM_ARCHIVE_FOLDER')
    start('SPIDERELEC','EAM_ARCHIVE_INFO')
    start('SPIDERELEC','EAM_CONFIG_SERIAL')

    # 四川省机关事务一体化服务平台内网门户
    start('SPIDERAPPLICATION','TB_MEETING_RECEIPT_INFO')

    # 数据中台系统
    start('SPIDERMONITI','RISK_INDICATOR_INFO')

    # 数据资源中心系统
    start('SPIDER','DGS_T_GWYC_QL')
    start('SPIDER','DGS_T_GYZCQL')
    start('SPIDER','DGS_T_ZCFLZD')

    # 综合业务办理系统
    start('IFRAMEWORK','BZ_ASSET_ARCHIVIST')
    start('IFRAMEWORK','BZ_ASSET_DISPOSAL_RECORD')
    start('IFRAMEWORK','I_FORM_DATA')
    start('IFRAMEWORK','I_FORM_DATA_RECEIPT')
    start('IFRAMEWORK','JBXX_INTERNET_ROLE')
    start('IFRAMEWORK','Y_APP_FILE_INFO')
    start('IFRAMEWORK','Y_FILE_INFO')
    start('IFRAMEWORK','BZ_ASSET')
    start('IFRAMEWORK','BZ_ASSET_ARCHIVIST')
    start('IFRAMEWORK','BZ_ASSET_DISPOSAL_RECORD')
    start('IFRAMEWORK','BZ_ASSET_HISTORY')

    # 政策法规系统系统
    start('ZCFG', 'POL_CONTRACT_ATTACHMENT')
    start('ZCFG', 'POL_CONTRACT_DOCUMENT')
    start('ZCFG', 'POL_CONTRACT_INFO')
    start('ZCFG', 'POL_DATA_INFO')
    start('ZCFG', 'POL_FINANCE_INFO')
    start('ZCFG', 'POL_PROJECT_APPLICATION')
    start('ZCFG', 'POL_PROJECT_RESEARCH')
    start('ZCFG', 'POL_REGULATIONS_INFO')
    start('ZCFG', 'POL_STANDARD_INFO')

    # 财务内控管理系统
    start('CWNK', 'FINANCE_BASIC_REVIEW_PROJECT_20241011BAK')

    # 幼儿园报名管理系统
    start('YOUERYUAN', 'KIN_ENROLLMENT_INFO')
