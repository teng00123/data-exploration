import json
from sqlalchemy import create_engine,text
username= 'root'
password = 'oneapimmysql'
database_address = '192.168.20.8'
prot = 3306
database_name = 'test'
table_name = 'mk_sc_waterp_result_table'


db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
engine = create_engine(db_url)
connection = engine.connect()
with open('1.json', 'r', encoding='utf-8') as f:
    data = f.read()
    result_data = json.loads(data)


sql = """
INSERT INTO {table_name} (tableEName, tableCName, dataItemCName,dataItemEName,dataItemType,dataItemLength,dataItemKey,dataItemEmpty,dBNumber) VALUES 
({tableEName}, {tableCName}, {dataItemCName}, {dataItemEName}, {dataItemType}, {dataItemLength}, {dataItemKey}, {dataItemEmpty}, {dBNumber})

"""

for data in result_data['column_list']:
    insert_sql = sql.format(
        table_name=table_name,
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
    print(insert_sql)
    connection.execute(text(insert_sql))
    connection.commit()

print('--------ok--------------')
