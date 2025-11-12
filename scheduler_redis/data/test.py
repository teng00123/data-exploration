from sqlalchemy import create_engine,text
import urllib.parse
import pandas as pd
username='sjtc'
password='WDoracle2019sjtcSC'
password = urllib.parse.quote_plus(password)
database_address='59.225.203.89'
prot='1551'
database_name='center'


db_url = f'oracle+cx_oracle://{username}:{password}@{database_address}:{prot}/?service_name={database_name}'
# db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
engine = create_engine(db_url)
connection = engine.connect()
username='root'
password='123456'
password = urllib.parse.quote_plus(password)
database_address='172.21.143.186'
prot='5432'
database_name='bsp-user'
db_url = f"postgresql://{username}:{password}@{database_address}:{prot}/{database_name}"
engine = create_engine(db_url)
pg_connection = engine.connect()


sql = """
select p.model_col_name,p.model_col_display_name,t.model_name,t.model_tab_name from cen_brmp.brmp_conf_origin_system_model p 
inner join cen_brmp.brmp_conf_origin_system_mdbase t
on p.model_id = t.model_id
"""
result = connection.execute(text(sql)).fetchall()
df = pd.DataFrame(result, columns=[
    "model_col_name",
    "model_col_display_name",
    "model_name",
    "model_tab_name"
]).to_dict(orient='records')
for table_info in df:
    update_table_sql = f"""
        update biz_data_directory set cn_name='{table_info["model_name"]}' where  system_id=81102651775 and en_name='{table_info["model_tab_name"].upper()}'

    """
    update_table_result = pg_connection.execute(text(update_table_sql))
    if update_table_result.rowcount == 0:
        print("没有找到匹配的行进行更新。")
        continue
    else:
        print(f"成功更新了 biz_data_directory {update_table_result.rowcount} 行。")
    table_sql = f"""
    select id from biz_data_directory where  system_id=81102651775 and en_name='{table_info["model_tab_name"].upper()}'
    """
    result = pg_connection.execute(text(table_sql)).fetchall()
    df = pd.DataFrame(result, columns=[
        "id"
    ]).to_dict(orient='records')
    field_sql = f"""
    update biz_data_directory_item set item_name='{table_info['model_col_display_name']}' where data_directory_id={df[0]['id']} and en_name='{table_info['model_col_name'].lower()}'
    
    """
    field_result = pg_connection.execute(text(field_sql))
    if field_result.rowcount == 0:
        print("没有找到匹配的行进行更新。")
    else:
        print(f"成功更新了 biz_data_directory_item {field_result.rowcount} 行。")
    pg_connection.commit()
