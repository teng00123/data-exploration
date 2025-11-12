import random
import uuid
import re

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker

from backend.database.sys_model import DataDirectoryShip
from backend.database.exploration_model import TableInfo, FieldInfo, TableAssociationInfo, DatabaseChangeLog, \
    DatasourceInfo, TableHistoryInfo, FieldHistoryInfo, BelongSystem, TableHistoryTemplateInfo
from backend.database.directory import DataDirectory, DataDirectoryItem
from sqlalchemy import create_engine, text
from backend.config import config
from datetime import datetime
import urllib.parse
import dmPython
from backend.database.schedule_info import ScheduleExecute
from typing import Union
from cryptography.fernet import Fernet
from backend.database.sys_model import DataDirectoryFieldShip
from backend.template.mapping import dmdb_mapping, oracle_mapping, mysql_mapping, sqlite_mapping, pgsql_mapping


def convert_format(data_list):
    result = []
    for item in data_list:
        column_name, data_type, data_length, data_precision, data_scale, nullable, comment = item
        nullable = True if nullable == 'Y' else False
        column_info = {
            'name': column_name.lower(),
            'type': data_type +"("+ str(data_length) + ')',
            'nullable': nullable,
            'default': None,
            'comment': comment
        }
        result.append(column_info)
    return result

def table_convert_format(item):
    table_name, table_comments = item
    column_info = {
        'table_name': table_name,
        'text': table_comments
    }
    return column_info


key = "GHiC1UXbXbu3tBN-x-K8ubLZdKImj-QzgR0Nmii2MYQ="
cipher_suite = Fernet(key)

# 加密
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

# 解密函数
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def process_field_type(
        field_type_str: Union[str],
        database_type: Union[str]) -> tuple:
    if database_type == 'dmdb':
        mapping = dmdb_mapping
        return dm_exec(field_type_str, mapping)
    if database_type == 'mysql':
        mapping = mysql_mapping
    if database_type == 'postgresql':
        mapping = pgsql_mapping
    if database_type == 'oracle':
        mapping = oracle_mapping
    if database_type == 'sqlite':
        mapping = sqlite_mapping
    # Remove collation part
    field_type_str = field_type_str.split('COLLATE')[0].strip()

    # Split to get type and length
    if '(' in field_type_str:
        type_part, length_part = field_type_str.split('(')
        length = length_part.rstrip(')')
    else:
        type_part = field_type_str
        length = None

    # Map to Chinese
    chinese_type = mapping.get(type_part, type_part)

    return chinese_type, length


def dm_exec(
        field_type: Union[str],
        mapping: Union[dict]) -> tuple:
    # 提取字段类型和长度
    full_type = field_type[0]
    # 找到第一个数字的位置
    number_index = re.search(r'\d', full_type).start()
    # 分割类型和长度
    field = full_type[:number_index]
    length = full_type[number_index:]

    # 映射到中文类型
    chinese_type = mapping.get(field, field)  # 如果没有映射，则使用原字段类型

    # 打印结果
    return chinese_type, length


def table_check_change(
        tables: Union[list],
        data: Union[dict],
        session
) -> None:
    """

    :param tables: 扫描数据库所有表信息
    :param data: 请求参数
    :return:
        检查删除更新状态的表
    """
    cur_database = session.query(TableInfo).filter_by(schedule_id=data.get('schedule_id'),is_delete=False).all()
    for table in cur_database:
        table_history_info = session.query(TableHistoryInfo).filter_by(id=table.table_history_id).first()
        field_change_log = session.query(DatabaseChangeLog).filter_by(table_info_id=table_history_info.id,change_type='field').filter(DatabaseChangeLog.change_status.in_(['update','add','delete'])).first()
        if table.table_name not in tables:
            change_status = 'delete'
            table.is_delete = True
        elif table_history_info.table_history_id is None:
            change_status = 'add'
        elif field_change_log or table_history_info.table_comment != table.table_comment:
            change_status = 'update'
        else:
            change_status = 'consistent'
        database_change = DatabaseChangeLog(
            schedule_info_id=data.get('schedule_id'),
            table_info_id=table.table_history_id,
            change_type='table',
            change_status=change_status
        )
        session.add(database_change)
        session.flush()
        print(database_change.change_status)

def generate_directory(data: Union[dict],session):
    table_infos = session.query(TableInfo).filter_by(schedule_id=data.get('schedule_id'),is_delete=False).all()
    system_info = session.query(BelongSystem).filter_by(id=data.get('system_id')).first()
    for table_info in table_infos:
        data_directory = session.query(DataDirectory).filter_by(table_id=table_info.id, datasource_id=table_info.datasource_id,
                                                       history=False).first()
        table_change = session.query(DatabaseChangeLog).filter_by(table_info_id=table_info.table_history_id,
                                                         schedule_info_id=data.get('schedule_id'),
                                                         change_type='table').first()
        main_data_directory = session.query(DataDirectory).filter_by(table_id=table_info.id, datasource_id=table_info.datasource_id).first()
        if not data_directory:
            id = random.randint(10 ** 17, 10 ** 18 - 1)
            main_version_id = id
            if main_data_directory:
                main_version_id = main_data_directory.main_version_id
            data_directory = DataDirectory(
                id=id,
                datasource_id=table_info.datasource_id,
                table_id=table_info.id,
                create_id=data.get('userId'),
                status=0,
                system_id=system_info.id,
                data_zie=table_info.data_total,
                cn_name=table_info.table_comment,
                contents_code=str(uuid.uuid4()),
                en_name=table_info.table_name,
                dept_id=system_info.department_id,
                data_provider=system_info.department,
                history=False,
                build_directory=True,
                data_version=1,
                data_source_mode='系统探查',
                main_version_id=main_version_id,
                data_storage_capacity=table_info.data_storage,
                create_time=datetime.now()
            )
            session.add(data_directory)
            session.flush()
            field_infos = session.query(FieldInfo).filter_by(table_info_id=table_info.id,is_delete=False).all()
            for field_info in field_infos:
                # item_type, length = process_field_type(field_info.type, data.get('database_type'))
                data_directory_item = DataDirectoryItem(
                    id=random.randint(10 ** 17, 10 ** 18 - 1),
                    table_info_id=table_info.id,
                    field_id=field_info.id,
                    en_name=field_info.name,
                    item_name=field_info.comment,
                    item_type=field_info.type,
                    primary_keys=field_info.primary_keys,
                    data_directory_id=data_directory.id,
                )
                session.add(data_directory_item)
            session.flush()
        else:
            if table_info.data_total is not None:
                data_directory.data_zie = table_info.data_total
            if table_info.data_storage is not None:
                data_directory.data_storage_capacity = table_info.data_storage
            if table_change.change_status == 'update':
                if int(data_directory.status) in (3, 4, 5, 6):
                    data_directory.history = True
                    data_version = data_directory.data_version + 1
                    cn_name = data_directory.cn_name
                    new_data_directory = DataDirectory(
                        id=random.randint(10 ** 17, 10 ** 18 - 1),
                        datasource_id=table_info.datasource_id,
                        table_id=table_info.id,
                        create_id=data_directory.create_id,
                        status=1,
                        system_id=data.get('system_id'),
                        data_level=data_directory.data_level,
                        summary=data_directory.summary,
                        up_cycle=data_directory.up_cycle,
                        data_zie=table_info.data_total,
                        cn_name=cn_name,
                        contents_code=data_directory.contents_code,
                        en_name=data_directory.en_name,
                        data_processing=data_directory.data_processing,
                        data_scope=data_directory.data_scope,
                        data_start_date_scope=data_directory.data_start_date_scope,
                        data_end_date_scope=data_directory.data_end_date_scope,
                        contact=data_directory.contact,
                        phone=data_directory.phone,
                        email=data_directory.email,
                        data_provider=data_directory.data_provider,
                        ywy_id=data_directory.ywy_id,
                        zty_id=data_directory.zty_id,
                        ydx_id=data_directory.ydx_id,
                        ywy_name=data_directory.ywy_name,
                        zty_name=data_directory.zty_name,
                        ydx_name=data_directory.ydx_name,
                        commit_time=data_directory.commit_time,
                        data_version_time=datetime.now(),
                        build_directory_result=data_directory.build_directory_result,
                        dept_id=data_directory.dept_id,
                        history=False,
                        build_directory=True,
                        data_storage_capacity=table_info.data_storage,
                        data_source_mode='系统探查',
                        data_version=data_version,
                        main_version_id=data_directory.main_version_id,
                        create_time=datetime.now()
                    )
                    session.add(new_data_directory)
                    session.flush()
                    old_data_directory_ships = session.query(DataDirectoryShip).filter_by(data_directory_id=data_directory.id).all()
                    for old_data_directory_ship in old_data_directory_ships:
                        new_data_directory_ship = DataDirectoryShip(
                            id=random.randint(10 ** 17, 10 ** 18 - 1),
                            data_directory_id=new_data_directory.id,
                            ship_id=old_data_directory_ship.ship_id,
                            create_id=old_data_directory_ship.create_id
                        )
                        session.add(new_data_directory_ship)
                        session.flush()
                    old_data_directory_field_ships = session.query(DataDirectoryFieldShip).filter_by(data_directory_id=data_directory.id).all()
                    for old_data_directory_field_ship in old_data_directory_field_ships:
                        new_data_directory_field_ship = DataDirectoryFieldShip(
                            id=random.randint(10 ** 17, 10 ** 18 - 1),
                            data_directory_id=new_data_directory.id,
                            field_id=old_data_directory_field_ship.field_id,
                            ship_data_directory_id=old_data_directory_field_ship.ship_data_directory_id,
                            field_name=old_data_directory_field_ship.field_name
                        )
                        session.add(new_data_directory_field_ship)
                        session.flush()
                    field_infos = session.query(FieldInfo).filter_by(table_info_id=table_info.id,is_delete=False).all()
                    for field_info in field_infos:
                        # item_type, length = process_field_type(field_info.type, data.get('database_type'))
                        en_name = field_info.name
                        primary_keys = field_info.primary_keys
                        old_data_directory_item = session.query(DataDirectoryItem).filter_by(field_id=field_info.id,table_info_id=data_directory.table_id,data_directory_id=data_directory.id).first()
                        if not old_data_directory_item or old_data_directory_item.item_name == '':
                            item_name = field_info.comment
                        else:
                            item_name = old_data_directory_item.item_name
                        if old_data_directory_item:
                            en_name = old_data_directory_item.en_name
                            primary_keys = old_data_directory_item.primary_keys
                        data_directory_item = DataDirectoryItem(
                            id=random.randint(10 ** 17, 10 ** 18 - 1),
                            table_info_id=table_info.id,
                            field_id=field_info.id,
                            en_name=en_name,
                            item_name=item_name,
                            item_type=field_info.type,
                            primary_keys=primary_keys,
                            data_directory_id=new_data_directory.id,
                        )
                        session.add(data_directory_item)
                    session.flush()
                else:
                    field_infos = session.query(FieldInfo).filter_by(table_info_id=table_info.id,is_delete=False).all()
                    if not data_directory.cn_name:
                        data_directory.cn_name = table_info.table_comment
                    data_directory.history = False
                    data_directory.update_time = datetime.now()
                    if data_directory.status == 2:
                        data_directory.status = 1
                    for field_info in field_infos:
                        field_history_info = session.query(FieldHistoryInfo).filter_by(table_info_id=table_info.table_history_id,name=field_info.name).first()
                        field_change_info = session.query(DatabaseChangeLog).filter_by(field_info_id=field_history_info.id,
                                                                              table_info_id=table_info.table_history_id,
                                                                              schedule_info_id=data.get('schedule_id'),
                                                                              change_type='field').first()
                        # item_type, length = process_field_type(field_info.type, data.get('database_type'))
                        if field_change_info.change_status == 'add':
                            data_directory_item = DataDirectoryItem(
                                id=random.randint(10 ** 17, 10 ** 18 - 1),
                                table_info_id=table_info.id,
                                field_id=field_info.id,
                                en_name=field_info.name,
                                item_name=field_info.comment,
                                item_type=field_info.type,
                                primary_keys=field_info.primary_keys,
                                data_directory_id=data_directory.id,
                            )
                            session.add(data_directory_item)
                            session.flush()
                        elif field_change_info.change_status == 'update':
                            data_directory_item = session.query(DataDirectoryItem).filter_by(table_info_id=table_info.id,field_id=field_info.id,data_directory_id=data_directory.id).first()
                            item_name = data_directory_item.item_name
                            if item_name == '' or item_name is None:
                                item_name = field_info.comment
                            data_directory_item.en_name=field_info.name
                            data_directory_item.item_name=item_name
                            data_directory_item.item_type=field_info.type
                            data_directory_item.primary_keys=field_info.primary_keys
                            session.add(data_directory_item)
                            session.flush()
                        elif field_change_info.change_status == 'delete':
                            data_directory_item = session.query(DataDirectoryItem).filter_by(table_info_id=table_info.id,
                                                                                    field_id=field_info.id,
                                                                                    data_directory_id=data_directory.id).first()
                            session.delete(data_directory_item)
                            session.flush()


def field_check_change(
        columns: Union[list],
        table_info_id: Union[int],
        data: Union[dict],
        session
) -> None:
    """

    :param columns: 扫描数据库表所有字段信息
    :param table_info_id: 信息目录表id
    :param data: 请求参数
    :return:
        检查删除更新状态的字段
    """
    history_table_info = session.query(TableHistoryInfo).join(TableInfo,TableHistoryInfo.id==TableInfo.table_history_id).filter_by(id=table_info_id).first()
    new_columns = session.query(FieldHistoryInfo).filter_by(table_info_id=history_table_info.id).all()
    old_columns = session.query(FieldHistoryInfo).filter_by(table_info_id=history_table_info.table_history_id).all()
    old_columns_name = [column.name for column in old_columns]
    new_columns_name = [column.name for column in new_columns]
    for column in new_columns:

        old_column = session.query(FieldHistoryInfo).filter_by(name=column.name,table_info_id=history_table_info.table_history_id).first()
        if not old_column:
            field_change_status = 'add'
        elif old_column.primary_keys != column.primary_keys or old_column.type != column.type or old_column.nullable != column.nullable or old_column.default != column.default or old_column.autoincrement != column.autoincrement or old_column.comment != column.comment:
            field_change_status = 'update'
        else:
            field_change_status = 'consistent'

        field_change = DatabaseChangeLog(
            schedule_info_id=data.get('schedule_id'),
            table_info_id=history_table_info.id,
            field_info_id=column.id,
            change_type='field',
            change_status=field_change_status)
        session.add(field_change)
        session.flush()
    difference = [x for x in old_columns_name if x not in new_columns_name]
    if difference:
        field_change_status = 'delete'
        for name in difference:
            field_info = session.query(FieldInfo).filter_by(table_info_id=table_info_id,name=name).first()
            field_info.is_delete = True
            field_change = DatabaseChangeLog(
                schedule_info_id=data.get('schedule_id'),
                table_info_id=history_table_info.id,
                change_type='field',
                change_status=field_change_status)
            session.add(field_change)
            session.flush()

def generate_table_template(schedule_execute_id,session):
    table_history_infos = session.query(TableHistoryInfo).filter_by(schedule_execute_id=schedule_execute_id).all()
    for table_history_info in table_history_infos:
        field_count = session.query(FieldHistoryInfo).filter_by(table_info_id=table_history_info.id).count()
        table_change = session.query(DatabaseChangeLog).filter_by(table_info_id=table_history_info.id,
                                                         change_type='table').first()
        table_history = session.query(TableHistoryInfo).filter_by(table_name=table_history_info.table_name,
                                                         datasource_id=table_history_info.datasource_id,
                                                         id=table_history_info.table_history_id).first()
        if table_history:
            try:
                data_total_change = int(table_history_info.data_total) - int(
                    table_history.data_total)
            except Exception as e:
                data_total_change = None
        else:
            data_total_change = 0
        status_order = {'add': 0, 'update': 1, 'consistent': 2}
        change_status = status_order[table_change.change_status]
        table_history_template_info = TableHistoryTemplateInfo(
            id=table_history_info.id,
            table_name=table_history_info.table_name,
            table_comment=table_history_info.table_comment,
            data_total=table_history_info.data_total,
            datasource_id=table_history_info.datasource_id,
            schedule_execute_id=table_history_info.schedule_execute_id,
            table_history_id=table_history_info.table_history_id,
            field_count=field_count,
            data_total_change=data_total_change,
            change_status=change_status
        )
        session.add(table_history_template_info)

# 数据探查用例
def _data_exploration(
        data: Union[dict]
) -> tuple:
    """

    :param data: request 请求参数
    :return: (状态码，结果)

    数据探查任务
    """

    from scheduler_redis.scheduler import logger

    sys_engine = create_engine(
        f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    session = sessionmaker(bind=sys_engine)()
    datasource_id = data.get('datasource_id')
    datasource_info = session.query(DatasourceInfo).filter_by(id=datasource_id).first()
    database_type = datasource_info.database_type
    username = datasource_info.database_username
    database_address = datasource_info.database_address
    password = urllib.parse.quote_plus(decrypt_password(datasource_info.database_password))
    if database_type == 'dmdb':
        password = decrypt_password(datasource_info.database_password)
    database_name = datasource_info.database_name
    schema_name = datasource_info.schema_name
    data['system_id'] = datasource_info.belonging_system_id
    schedule_execute = ScheduleExecute(
        datasource_id=datasource_id,
        schedule_name=data.get('schedule_name'),
        schedule_id=data.get('schedule_id'),
        schedule_time=int(datetime.now().timestamp()),
        schedule_status='执行中'
    )

    session.add(schedule_execute)
    session.commit()
    try:
        if database_type == 'mysql':
            db_url = f"mysql+pymysql://{username}:{password}@{database_address}/{database_name}"
            count_query = 'SELECT COUNT(1) FROM `{table_name}`'
        if database_type == 'postgresql':
            db_url = f"postgresql://{username}:{password}@{database_address}/{database_name}"
            count_query = 'SELECT COUNT(1) FROM {schema_name}.{table_name}'
        if database_type == 'sqlite':
            db_url = f'sqlite:///{database_address}'
            count_query = 'SELECT COUNT(1) FROM "{table_name}"'
        if database_type == 'sql_server':
            db_url = f'mssql+pyodbc://{username}:{password}@{database_address}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
            count_query = 'SELECT COUNT(1) FROM {table_name}'
        if database_type == 'oracle':
            db_url = f'oracle+cx_oracle://{username}:{password}@{database_address}/?service_name={database_name}'
            engine = create_engine(db_url)
            connection = engine.connect()
            count_query = 'SELECT COUNT(1) FROM {schema_name}.{table_name}'
            sql_query = f"SELECT table_name FROM all_tables where owner = '{schema_name.upper()}'"
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

            result = connection.execute(text(sql_query)).fetchall()
            table_names = [i[0] for i in result]
            for table_name in table_names:
                table_info = session.query(TableInfo).filter_by(
                    datasource_id=datasource_id,
                    schedule_id=data.get('schedule_id'),
                    table_name=table_name,
                    is_delete=False).first()
                constrained_columns = [i[0] for i in connection.execute(text(constrain_query.format(table_name=table_name))).fetchall()]
                columns = convert_format(connection.execute(text(columns_query.format(table_name=table_name))).fetchall())
                columns = [{**item, 'type': str(item['type'])} for item in columns]
                logger.info(str(columns))
                try:
                    table_comment = table_convert_format(connection.execute(text(table_comment_query.format(table_name=table_name, schema_name=schema_name.upper()))).fetchone())
                except Exception as e:
                    table_comment = {}
                try:
                    table_data_count = \
                        engine.connect().execute(text(count_query.format(schema_name=schema_name.upper(),table_name=table_name.upper()))).fetchone()[
                            0]
                except Exception as e:
                    table_data_count = None

                try:
                    table_datastorge_count = \
                        engine.connect().execute(text(table_datastorge_query.format(schema_name=schema_name.upper(),table_name=table_name.upper()))).fetchone()[
                            0]
                except Exception as e:
                    table_datastorge_count = None
                logger.info(str(table_datastorge_count))
                if not table_info:
                    table_info = TableInfo(
                        datasource_id=datasource_id,
                        schedule_id=data.get('schedule_id'),
                        table_name=table_name,
                        data_total=table_data_count,
                        table_comment=table_comment.get('text'),
                        data_storage=table_datastorge_count
                    )
                    session.add(table_info)
                    session.flush()
                    table_history_info = TableHistoryInfo(
                        datasource_id=datasource_id,
                        schedule_execute_id=schedule_execute.id,
                        table_name=table_name,
                        data_total=table_data_count,
                        table_comment=table_comment.get('text'),
                        data_storage=table_datastorge_count
                    )
                    session.add(table_history_info)
                    session.flush()
                    table_info.table_history_id = table_history_info.id
                else:
                    table_info.data_total = table_data_count
                    table_info.table_comment = table_comment.get('text')
                    table_info.update_time = int(datetime.now().timestamp())
                    table_history_info = TableHistoryInfo(
                        datasource_id=datasource_id,
                        schedule_execute_id=schedule_execute.id,
                        table_name=table_name,
                        data_total=table_data_count,
                        table_comment=table_comment.get('text'),
                        table_history_id=table_info.table_history_id,
                        data_storage=table_datastorge_count
                    )
                    session.add(table_history_info)
                    session.flush()
                    table_info.table_history_id = table_history_info.id
                    session.flush()
                for column in columns:
                    if column.get('name').upper() in constrained_columns:
                        primary_keys = True
                    else:
                        primary_keys = False
                    field_info = session.query(FieldInfo).filter_by(
                        table_info_id=table_info.id,
                        name=column.get('name'),
                        is_delete=False
                    ).first()
                    if not field_info:
                        field_info = FieldInfo(
                            table_info_id=table_info.id,
                            name=column.get('name'),
                            primary_keys=primary_keys,
                            type=column.get('type'),
                            nullable=column.get('nullable'),
                            default=column.get('default'),
                            autoincrement=column.get('autoincrement'),
                            comment=column.get('comment')
                        )
                        session.add(field_info)
                        session.flush()
                    else:
                        field_info.comment = column.get('comment')
                        field_info.type = column.get('type')
                        field_info.update_time = int(datetime.now().timestamp())
                    field_history_info = FieldHistoryInfo(
                        table_info_id=table_history_info.id,
                        name=column.get('name'),
                        primary_keys=primary_keys,
                        type=column.get('type'),
                        nullable=column.get('nullable'),
                        default=column.get('default'),
                        autoincrement=column.get('autoincrement'),
                        comment=column.get('comment')
                    )
                    session.add(field_history_info)
                    session.flush()
                field_check_change(columns, table_info.id, data, session)
            table_check_change(table_names, data, session)
            engine.dispose()
        elif database_type == 'dmdb':
            server = database_address.split(':')
            conn = dmPython.connect(user=username, password=password, server=server[0], port=server[1],connection_timeout=30000,login_timeout=30000)
            cursor = conn.cursor()
            cursor.execute(
                f"select table_name, comments from dba_tab_comments where table_type='TABLE' and owner = '{database_name}'")
            tab_comments_list = cursor.fetchall()
            for table_name,table_comment in tab_comments_list:
                table_info = session.query(TableInfo).filter_by(
                    datasource_id=datasource_id,
                    schedule_id=data.get('schedule_id'),
                    table_name=table_name).first()
                sql = f"""
                SELECT count(1) FROM "{database_name}"."{table_name}"
                """
                cursor.execute(sql)
                data_total = cursor.fetchone()[0]
                if not table_info:
                    new_table = True
                    table_info = TableInfo(
                        datasource_id=datasource_id,
                        schedule_id=data.get('schedule_id'),
                        table_name=table_name,
                        data_total=data_total,
                        table_comment=table_comment
                    )
                    session.add(table_info)
                    session.flush()
                    table_history_info = TableHistoryInfo(
                        datasource_id=datasource_id,
                        table_name=table_name,
                        data_total=data_total,
                        table_comment=table_comment,
                        schedule_execute_id=schedule_execute.id
                    )
                    session.add(table_history_info)
                    session.flush()
                    table_info.table_history_id = table_history_info.id
                else:
                    new_table = False
                    table_info.table_comment = table_comment
                    table_info.data_total = data_total
                    table_history_info = TableHistoryInfo(
                        datasource_id=datasource_id,
                        table_name=table_name,
                        data_total=data_total,
                        table_comment=table_comment,
                        schedule_execute_id=schedule_execute.id,
                        table_history_id=table_info.table_history_id
                    )
                    session.add(table_history_info)
                    session.flush()
                    table_info.table_history_id = table_history_info.id
                    session.flush()
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
                    dict_columns['type'] = dict_columns['data_type'] + str(dict_columns['data_length'])
                # field_check_change(columns_list, table_info.id, data)
                for merged in merged_info:
                    field_info = session.query(FieldInfo).filter_by(table_info_id=table_info.id, name=merged[1],
                                                           is_delete=False).first()
                    nullable = False if merged[6] == 'N' else True
                    primary = True if merged[1] == constraints_column else False
                    if not field_info:
                        field_info = FieldInfo(
                            table_info_id=table_info.id,
                            name=merged[1],
                            primary_keys=primary,
                            type=merged[2] + str(merged[3]),
                            nullable=nullable,
                            comment=merged[8]
                        )
                        session.add(field_info)
                        session.flush()
                    else:
                        field_info.type = merged[2] + str(merged[3])
                        field_info.nullable = nullable
                        field_info.comment = merged[8]
                    field_history_info = FieldHistoryInfo(
                        table_info_id=table_history_info.id,
                        name=merged[1],
                        primary_keys=primary,
                        type=merged[2] + str(merged[3]),
                        nullable=nullable,
                        comment=merged[8]
                    )
                    session.add(field_history_info)
                    session.flush()
                field_check_change(columns, table_info.id, data,session)
            table_check_change([table[0] for table in tab_comments_list], data,session)
        else:
            engine = create_engine(db_url)
            inspector = inspect(engine)
            table_names = inspector.get_table_names(schema=schema_name)
            for table_name in table_names:
                logger.info(count_query.format(schema_name=schema_name, table_name=table_name))
                table_info = session.query(TableInfo).filter_by(
                    datasource_id=datasource_id,
                    schedule_id=data.get('schedule_id'),
                    table_name=table_name,
                    is_delete=False).first()
                try:
                        constrained_columns = inspector.get_pk_constraint(table_name,schema=schema_name)
                except Exception as e:
                    continue
                columns = inspector.get_columns(table_name,schema=schema_name)
                columns = [{**item, 'type': str(item['type'])} for item in columns]
                try:
                    table_comment = inspector.get_table_comment(table_name,schema=schema_name)
                except Exception as e:
                    table_comment = {}
                try:

                    if database_type == 'postgresql':
                        table_data_count = \
                            engine.connect().execute(text(count_query.format(schema_name=schema_name,table_name=table_name))).fetchone()[
                                0]
                    else:
                        table_data_count = \
                            engine.connect().execute(text(count_query.format(table_name=table_name))).fetchone()[
                                0]
                except Exception as e:
                    logger.info(str(e))
                    table_data_count = None
                if not table_info:
                    table_info = TableInfo(
                        datasource_id=datasource_id,
                        schedule_id=data.get('schedule_id'),
                        table_name=table_name,
                        data_total=table_data_count,
                        table_comment=table_comment.get('text')
                    )
                    session.add(table_info)
                    session.flush()
                    table_history_info = TableHistoryInfo(
                        datasource_id=datasource_id,
                        schedule_execute_id=schedule_execute.id,
                        table_name=table_name,
                        data_total=table_data_count,
                        table_comment=table_comment.get('text')
                    )
                    session.add(table_history_info)
                    session.flush()
                    table_info.table_history_id = table_history_info.id
                else:
                    table_info.data_total = table_data_count
                    table_info.table_comment = table_comment.get('text')
                    table_info.update_time = int(datetime.now().timestamp())
                    table_history_info = TableHistoryInfo(
                        datasource_id=datasource_id,
                        schedule_execute_id=schedule_execute.id,
                        table_name=table_name,
                        data_total=table_data_count,
                        table_comment=table_comment.get('text'),
                        table_history_id=table_info.table_history_id
                    )
                    session.add(table_history_info)
                    session.flush()
                    table_info.table_history_id = table_history_info.id
                    session.flush()
                for column in columns:
                    if column.get('name') in constrained_columns.get('constrained_columns'):
                        primary_keys = True
                    else:
                        primary_keys = False
                    field_info = session.query(FieldInfo).filter_by(
                        table_info_id=table_info.id,
                        name=column.get('name'),
                        is_delete=False
                    ).first()
                    if not field_info:
                        field_info = FieldInfo(
                            table_info_id=table_info.id,
                            name=column.get('name'),
                            primary_keys=primary_keys,
                            type=column.get('type'),
                            nullable=column.get('nullable'),
                            default=column.get('default'),
                            autoincrement=column.get('autoincrement'),
                            comment=column.get('comment')
                        )
                        session.add(field_info)
                        session.flush()
                    else:
                        field_info.comment = column.get('comment')
                        field_info.type = column.get('type')
                        field_info.update_time = int(datetime.now().timestamp())
                    field_history_info = FieldHistoryInfo(
                        table_info_id=table_history_info.id,
                        name=column.get('name'),
                        primary_keys=primary_keys,
                        type=column.get('type'),
                        nullable=column.get('nullable'),
                        default=column.get('default'),
                        autoincrement=column.get('autoincrement'),
                        comment=column.get('comment')
                    )
                    session.add(field_history_info)
                    session.flush()
                field_check_change(columns, table_info.id, data,session)
            table_check_change(table_names, data,session)
            engine.dispose()
        generate_table_template(schedule_execute.id,session)
        data['database_type'] = database_type
        generate_directory(data,session)
        schedule_execute.schedule_status = '成功'
        schedule_execute.end_time = int(datetime.now().timestamp())
        schedule_execute.time_consuming = int(schedule_execute.end_time) - int(schedule_execute.schedule_time)
        session.commit()
        return (200, 'ok')
    except Exception as e:
        session.rollback()
        schedule_execute.schedule_status = '失败'
        schedule_execute.failure_reason = str(e)
        schedule_execute.end_time = int(datetime.now().timestamp())
        schedule_execute.time_consuming = int(schedule_execute.end_time) - int(schedule_execute.schedule_time)
        session.commit()
        return (203, str(e))
    finally:
        session.close()
        sys_engine.dispose()
