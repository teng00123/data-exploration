import random
import time
import uuid
import re

from sqlalchemy.orm import sessionmaker
from backend.database.sys_model import DataDirectoryFieldShip
from backend.database.sys_model import DataDirectoryShip
from backend.database.exploration_model import TableInfo, FieldInfo, DatabaseChangeLog, \
    DatasourceInfo, TableHistoryInfo, FieldHistoryInfo, BelongSystem, TableHistoryTemplateInfo
from backend.database.directory import DataDirectory, DataDirectoryItem
from sqlalchemy import create_engine, text
from backend.config import config
from datetime import datetime
import urllib.parse
from backend.database.schedule_info import ScheduleExecute
from typing import Union
from cryptography.fernet import Fernet
import pandas as pd


key = "GHiC1UXbXbu3tBN-x-K8ubLZdKImj-QzgR0Nmii2MYQ="
cipher_suite = Fernet(key)

# 解密函数
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def field_check_change(
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
    old_columns_dict = {column.name:column for column in old_columns}
    for column in new_columns:
        old_column = old_columns_dict.get(column.name, None)
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
        # print(database_change.change_status)


def generate_table_template(schedule_id,schedule_execute_id,session):
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
        table_history_template_info = session.query(TableHistoryTemplateInfo).filter_by(id=table_history_info.id).first()
        if not table_history_template_info:
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
        else:
            table_history_template_info.change_status = change_status
            table_history_template_info.data_total_change = data_total_change
            table_history_template_info.field_count=field_count

def generate_directory(data: Union[dict],session):
    from scheduler_redis.scheduler import logger

    table_infos = session.query(TableInfo).filter_by(schedule_id=data.get('schedule_id'),is_delete=False).all()
    system_info = session.query(BelongSystem).filter_by(id=data.get('system_id')).first()
    for table_info in table_infos:
        data_directory = session.query(DataDirectory).filter_by(table_id=table_info.id, datasource_id=table_info.datasource_id,
                                                       history=False).first()
        table_change = session.query(DatabaseChangeLog).filter_by(table_info_id=table_info.table_history_id,
                                                         schedule_info_id=data.get('schedule_id'),
                                                         change_type='table').first()
        print('table_change:'+str(table_change))
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
                data_source_mode='结果表探查',
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
                        data_source_mode='结果表探查',
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
                        print(old_data_directory_item)
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
                        logger.info(str(session.query(FieldHistoryInfo).filter_by(name=field_info.name).all()))
                        field_change_info = session.query(DatabaseChangeLog).filter_by(field_info_id=field_history_info.id,
                                                                              table_info_id=table_info.table_history_id,
                                                                              schedule_info_id=data.get('schedule_id'),
                                                                              change_type='field').first()
                        print('field_change:'+str(field_change_info))
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
                            if data_directory_item is None:
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
                            else:
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


def result_data_exploration(data: Union[dict]):
    from scheduler_redis.scheduler import logger
    try:
        logger.info(urllib.parse.quote_plus(config["database"]["password"]))
        sys_engine = create_engine(
            f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
        session = sessionmaker(bind=sys_engine)()
        datasource_id = data.get('datasource_id')
        datasource_info = session.query(DatasourceInfo).filter_by(id=datasource_id).first()
        database_type = datasource_info.database_type
        username = datasource_info.database_username
        database_address = datasource_info.database_address
        password = urllib.parse.quote_plus(decrypt_password(datasource_info.database_password))
        # password = '123456'
        database_name = datasource_info.database_name
        table_name = datasource_info.table_name
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

        if database_type == 'mysql':
            db_url = f"mysql+pymysql://{username}:{password}@{database_address}/{database_name}"
            table_info_query = f"""
                    SELECT 
                   tableEName,
                   tableCName,
                   dBNumber,
                   storageCapacity
            FROM {table_name} GROUP BY tableEName, tableCName, dBNumber, storageCapacity
                """
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
        if database_type == 'postgresql':
            db_url = f"postgresql://{username}:{password}@{database_address}/{database_name}"
            table_info_query = f"""
                    SELECT 
                           "tableEName",
                           "tableCName",
                           "dBNumber",
                           "storageCapacity"
                    FROM {table_name} GROUP BY "tableEName", "tableCName", "dBNumber" ,"storageCapacity"
                """
            field_info_query = """
                    SELECT
                           "dataItemEName",
                           "dataItemType",
                           "dataItemLength",
                           "dataItemEmpty",
                           "dataItemKey",
                           "dataItemCName"
                    FROM {table_name} WHERE "tableEName" = '{tableEName}'
                """
        engine = create_engine(db_url)
        connection = engine.connect()

        result = connection.execute(text(table_info_query)).fetchall()
        df = pd.DataFrame(result, columns=[
            "tableEName",
            "tableCName",
            "dBNumber",
            "storageCapacity"
        ])

        # 将 DataFrame 转换为字典列表
        result_dict = df.to_dict(orient='records')
        # 打印结果
        # print(result_dict)
        for record in result_dict:
            print(record)
            result = connection.execute(text(field_info_query.format(table_name=table_name,tableEName=record.get('tableEName')))).fetchall()
            df = pd.DataFrame(result, columns=[
                "dataItemEName",
                "dataItemType",
                "dataItemLength",
                "dataItemEmpty",
                "dataItemKey",
                "dataItemCName"
            ])
            result_field_dict = df.to_dict(orient='records')
            table_info = session.query(TableInfo).filter_by(
                datasource_id=datasource_id,
                schedule_id=data.get('schedule_id'),
                table_name=record.get('tableEName'),
                is_delete=False).first()
            if not table_info:
                table_info = TableInfo(
                    datasource_id=datasource_id,
                    schedule_id=data.get('schedule_id'),
                    table_name=record.get('tableEName'),
                    data_total=record.get('dBNumber'),
                    table_comment=record.get('tableCName'),
                    data_storage=record.get('storageCapacity')
                )
                session.add(table_info)
                session.flush()
                # print(table_info.table_name)
                table_history_info = TableHistoryInfo(
                    datasource_id=datasource_id,
                    schedule_execute_id=schedule_execute.id,
                    table_name=record.get('tableEName'),
                    data_total=record.get('dBNumber'),
                    table_comment=record.get('tableCName'),
                    data_storage=record.get('storageCapacity')
                )
                session.add(table_history_info)
                session.flush()
                table_info.table_history_id = table_history_info.id
            else:
                table_info.data_total = record.get('dBNumber')
                table_info.data_storage = record.get('storageCapacity')
                table_info.table_comment = record.get('tableCName')
                table_info.update_time = int(datetime.now().timestamp())
                table_history_info = TableHistoryInfo(
                    datasource_id=datasource_id,
                    schedule_execute_id=schedule_execute.id,
                    table_name=record.get('tableEName'),
                    data_total=record.get('dBNumber'),
                    table_comment=record.get('tableCName'),
                    table_history_id=table_info.table_history_id,
                    data_storage=record.get('storageCapacity')
                )
                session.add(table_history_info)
                session.flush()
                table_info.table_history_id = table_history_info.id
                session.flush()
            for column in result_field_dict:
                item_length = str(column.get('dataItemLength')) if column.get('dataItemLength') !=None else ''
                item_type = column['dataItemType'] + '(' + item_length + ')'
                field_info = session.query(FieldInfo).filter_by(
                    table_info_id=table_info.id,
                    name=column.get('dataItemEName'),
                    is_delete=False
                ).first()
                if not field_info:
                    field_info = FieldInfo(
                        table_info_id=table_info.id,
                        name=column.get('dataItemEName'),
                        primary_keys=False if column.get('dataItemKey') == '否' else True,
                        type=item_type,
                        nullable=False if column.get('dataItemEmpty') == '否' else True,
                        comment=column.get('dataItemCName')
                    )
                    session.add(field_info)
                    session.flush()
                else:
                    field_info.comment = column.get('dataItemEName')
                    field_info.type = item_type,
                    field_info.update_time = int(datetime.now().timestamp())
                field_history_info = FieldHistoryInfo(
                    table_info_id=table_history_info.id,
                    name=column.get('dataItemEName'),
                    primary_keys=False if column.get('dataItemKey') == '否' else True,
                    type=item_type,
                    nullable=False if column.get('dataItemEmpty') == '否' else True,
                    comment=column.get('dataItemCName')
                )
                session.add(field_history_info)
                session.flush()
            field_check_change(table_info.id, data, session)
            # print([i['tableEName'] for i in result_dict])
        table_check_change([i['tableEName'] for i in result_dict], data, session)
        print('table_over--------------------------------------------------------')
        engine.dispose()
        generate_table_template(data.get('schedule_id'),schedule_execute.id, session)
        print('generate_table_template_over--------------------------------------------------------')
        data['database_type'] = database_type
        generate_directory(data, session)
        print('generate_directory_over--------------------------------------------------------')
        schedule_execute.schedule_status = '成功'
        schedule_execute.end_time = int(datetime.now().timestamp())
        schedule_execute.time_consuming = int(schedule_execute.end_time) - int(schedule_execute.schedule_time)
        session.commit()
    except Exception as e:
        print(e)
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

if __name__ == '__main__':
    result_data_exploration({'schedule_ids': [425], 'userId': '1', 'deptId': '4', 'datasource_id': 508, 'schedule_id': 425, 'schedule_name': '四川省医院等级评审管理系统（智慧医院）数据库scsyydjpsglxt01_result_table', 'schedule_type': 'immediately'}
)