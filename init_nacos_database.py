import psycopg2
from typing import Union
from sqlalchemy import create_engine,text
from backend.config import BASE_DIR,config




def create_database(
        database_name: Union[str],
        database_address: Union[str]
) -> None:
    db_name_exist = """
    select * from pg_database where datname='{}';
    """.format(database_name)
    db_name = """
    CREATE DATABASE {};
    """.format(database_name)
    conn = psycopg2.connect(database_address)
    cur = conn.cursor()
    cur.execute(db_name_exist)
    conn.commit()  # <-- ADD THIS LINE
    result = cur.fetchall()
    if result == []:
        conn.autocommit = True
        cur.execute(db_name)
        conn.autocommit = False
    else:
        print('{} is exist'.format(database_name))
    cur.close()
    conn.close()

def insert_nacos_data() -> None:
    engine = create_engine(f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}:{config["database"]["port"]}/nacos')
    with open(rf"{BASE_DIR}/sql/nacos.sql", 'r', encoding='utf-8') as f:
        with engine.connect() as connection:
            connection.execute(text(f.read().replace(":",r"\:")))
            connection.commit()

def insert_user_data() -> None:
    engine = create_engine(f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    with open(rf"{BASE_DIR}/sql/bsp-user.sql",'r',encoding='utf-8') as f:
        with engine.connect() as connection:
            connection.execute(text(f.read().replace(":",r"\:")))
            connection.commit()

def init_nacos_database() -> None:
    create_database('test', f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}:{config["database"]["port"]}/postgres')
    insert_nacos_data()
    insert_user_data()

if __name__ == '__main__':
    init_nacos_database()
