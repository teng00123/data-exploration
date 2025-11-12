from sqlalchemy import create_engine, text
import urllib.parse
import pandas as pd
from sqlalchemy.inspection import inspect

username = 'sjpc001'
password = 'sjpc@1&yjt!SJ'
password = urllib.parse.quote_plus(password)
database_address = '59.225.206.73'
prot = '14106'
database_name = 'kjt_sjpc_result_table_database'
schema_name = None

db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
# db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
engine = create_engine(db_url)
connection = engine.connect()
inspector = inspect(engine)
table_names = inspector.get_table_names(schema=schema_name)
# print(table_names)
sql_query = f"SELECT table_name FROM all_tables where owner='GZJG'"
field_info_query = """
        SELECT
               dataItemEName,
               dataItemType,
               dataItemLength,
               dataItemEmpty,
               dataItemKey,
               dataItemCName
        FROM {table_name} WHERE tableEName = '{tableEName}'
    """
result = connection.execute(text(field_info_query.format(table_name='kjt_scskycxjsxt_result_table',tableEName='badcredits'))).fetchall()
print(result)