from sqlalchemy import create_engine, text
import urllib.parse
import pandas as pd

username = 'hii'
password = 'hii_2019'
password = urllib.parse.quote_plus(password)
database_address = '172.18.218.211'
prot = '10521'
database_name = 'SCYPT'
schema_name = 'SYSTEMMANAGE2020'

db_url = f'oracle+cx_oracle://{username}:{password}@{database_address}:{prot}/?service_name={database_name}'
# db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
engine = create_engine(db_url)
connection = engine.connect()
sql_query = f"SELECT table_name FROM all_tables where owner='GZJG'"
result = connection.execute(text(sql_query)).fetchall()
print(result)