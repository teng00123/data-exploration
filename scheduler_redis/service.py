import dmPython

from datetime import datetime

from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine, text

from typing import Union

from scheduler_redis.sql_template import SqlTemplate

from backend.database.sys_model import DataDirectoryShip
from backend.database.exploration_model import TableInfo, FieldInfo, TableAssociationInfo, DatabaseChangeLog, \
    DatasourceInfo, TableHistoryInfo, FieldHistoryInfo, BelongSystem, TableHistoryTemplateInfo
from backend.database.directory import DataDirectory, DataDirectoryItem


class DbService:

    @classmethod
    def create_table(cls, session, model, **kwargs):
        """
        通用的表数据插入方法

        :param session: sqlalchemy会话
        :param model: 要插入的模型类
        :param data: 包含字段值的字典
        :param kwargs: 额外的字段值
        :return: 插入的记录对象
        """
        # print(**kwargs)
        record = model(**kwargs)

        session.add(record)
        session.flush()
        return record

    @classmethod
    def create_table_commit(cls, session, model, **kwargs):
        """
        通用的表数据插入方法

        :param session: sqlalchemy会话
        :param model: 要插入的模型类
        :param data: 包含字段值的字典
        :param kwargs: 额外的字段值
        :return: 插入的记录对象
        """
        # print(**kwargs)
        record = model(**kwargs)

        session.add(record)
        session.commit()
        return record

    @classmethod
    def update_record(cls, session, model, **kwargs):
        """
        通用的表数据更新方法

        :param session: sqlalchemy会话
        :param model: 要更新的模型类
        :param record_id: 要更新的记录ID
        :param kwargs: 要更新的字段和值
        :return: 更新后的记录对象
        """
        for key, value in kwargs.items():
            setattr(model, key, value)

        session.commit()
        return record

    @classmethod
    def query_records(cls, session, model, filters=None, order_by=None, limit=None, filter=None):
        """
        通用的表数据查询方法

        :param session: sqlalchemy会话
        :param model: 要查询的模型类
        :param filters: 查询条件字典，例如 {'name': 'Alice', 'age': 25}
        :param order_by: 排序条件，例如 'name' 或 '-age'（降序）
        :param limit: 返回记录的最大数量
        :param filter: filter查询条件，例如 DatabaseChangeLog.change_status.in_(['update', 'add', 'delete'])
        :return: 查询结果列表
        """
        query = session.query(model)

        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(model, key) == value)

        if filter:
            query = query.filter(filter)

        # 应用排序条件
        if order_by:
            if order_by.startswith('-'):
                column = getattr(model, order_by[1:])
                query = query.order_by(column.desc())
            else:
                query = query.order_by(getattr(model, order_by))

        # 应用限制条件
        if limit:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def query_records_first(cls, session, model, filters=None, order_by=None, limit=None, filter=None):
        """
        通用的表数据查询方法(单条)

        :param session: sqlalchemy会话
        :param model: 要查询的模型类
        :param filters: 查询条件字典，例如 {'name': 'Alice', 'age': 25}
        :param order_by: 排序条件，例如 'name' 或 '-age'（降序）
        :param limit: 返回记录的最大数量
        :param filter: filter查询条件，例如 DatabaseChangeLog.change_status.in_(['update', 'add', 'delete'])
        :return: 查询结果列表
        """
        query = session.query(model)

        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(model, key) == value)

        if filter:
            query = query.filter(filter)

        # 应用排序条件
        if order_by:
            if order_by.startswith('-'):
                column = getattr(model, order_by[1:])
                query = query.order_by(column.desc())
            else:
                query = query.order_by(getattr(model, order_by))

        # 应用限制条件
        if limit:
            query = query.limit(limit)

        return query.first()


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
    cur_database = DbService.query_records(session, TableInfo, filters={'schedule_id': data.get('schedule_id'), 'is_delete': False})
    for table in cur_database:
        table_history_info = DbService.query_records_first(session, TableHistoryInfo, filters={'id': table.table_history_id})
        field_change_log = DbService.query_records_first(session, DatabaseChangeLog, filters={'table_info_id': table_history_info.id,
                                                                      'change_type': 'field'},filter=DatabaseChangeLog.change_status.in_(['update', 'add', 'delete']))
        if table.table_name not in tables:
            change_status = 'delete'
            table.is_delete = True
        elif table_history_info.table_history_id is None:
            change_status = 'add'
        elif field_change_log or table_history_info.table_comment != table.table_comment:
            change_status = 'update'
        else:
            change_status = 'consistent'
        DbService.create_table(
            session,
            DatabaseChangeLog,
            schedule_info_id=data.get('schedule_id'),
            table_info_id=table.table_history_id,
            change_type='table',
            change_status=change_status
        )


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
    history_table_info = session.query(TableHistoryInfo).join(TableInfo,
                                                              TableHistoryInfo.id == TableInfo.table_history_id).filter_by(
        id=table_info_id).first()
    new_columns = DbService.query_records(session, FieldHistoryInfo, filters={'table_info_id': history_table_info.id})
    old_columns = DbService.query_records(session, FieldHistoryInfo, filters={'table_info_id': history_table_info.table_history_id})
    old_columns_name = [column.name for column in old_columns]
    new_columns_name = [column.name for column in new_columns]
    old_columns_dict = {column.name: column for column in old_columns}
    for column in new_columns:
        old_column = old_columns_dict.get(column.name, None)
        if not old_column:
            field_change_status = 'add'
        elif old_column.primary_keys != column.primary_keys or old_column.type != column.type or old_column.nullable != column.nullable or old_column.default != column.default or old_column.autoincrement != column.autoincrement or old_column.comment != column.comment:
            field_change_status = 'update'
        else:
            field_change_status = 'consistent'
        DbService.create_table(
            session,
            DatabaseChangeLog,
            schedule_info_id=data.get('schedule_id'),
            table_info_id=history_table_info.id,
            field_info_id=column.id,
            change_type='field',
            change_status=field_change_status
        )
    difference = [x for x in old_columns_name if x not in new_columns_name]
    if difference:
        field_change_status = 'delete'
        for name in difference:
            field_info = DbService.query_records_first(session,FieldInfo, filters={'table_info_id': table_info_id, 'name': name})
            field_info.is_delete = True
            DbService.create_table(
                session,
                DatabaseChangeLog,
                schedule_info_id=data.get('schedule_id'),
                table_info_id=history_table_info.id,
                change_type='field',
                change_status=field_change_status
            )


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



class DataExplorationService:

    @classmethod
    def general_exploration(cls, db_url, count_query, schema_name, data, datasource_id, database_type, session,
                            schedule_execute):
        engine = create_engine(db_url)
        inspector = inspect(engine)
        table_names = inspector.get_table_names(schema=schema_name)
        for table_name in table_names:
            table_info = session.query(TableInfo).filter_by(
                datasource_id=datasource_id,
                schedule_id=data.get('schedule_id'),
                table_name=table_name,
                is_delete=False).first()
            try:
                constrained_columns = inspector.get_pk_constraint(table_name, schema=schema_name)
            except Exception as e:
                continue
            columns = inspector.get_columns(table_name, schema=schema_name)
            columns = [{**item, 'type': str(item['type'])} for item in columns]
            try:
                table_comment = inspector.get_table_comment(table_name, schema=schema_name)
            except Exception as e:
                table_comment = {}
            try:

                if database_type == 'postgresql':
                    table_data_count = \
                        engine.connect().execute(
                            text(count_query.format(schema_name=schema_name, table_name=table_name))).fetchone()[
                            0]
                else:
                    table_data_count = \
                        engine.connect().execute(text(count_query.format(table_name=table_name))).fetchone()[
                            0]
            except Exception as e:
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
            field_check_change(table_info.id, data, session)
        table_check_change(table_names, data, session)
        engine.dispose()


    @classmethod
    def oracle_exploration(cls,db_url,datasource_id,schema_name,count_query,data,schedule_execute,session):

        engine = create_engine(db_url)
        connection = engine.connect()
        sql_query = f"SELECT table_name FROM all_tables where owner = '{schema_name.upper()}'"
        result = connection.execute(text(sql_query)).fetchall()
        table_names = [i[0] for i in result]
        for table_name in table_names:
            table_info = session.query(TableInfo).filter_by(
                datasource_id=datasource_id,
                schedule_id=data.get('schedule_id'),
                table_name=table_name,
                is_delete=False).first()
            constrained_columns = [i[0] for i in
                                   connection.execute(text(SqlTemplate.constrain_query.format(table_name=table_name))).fetchall()]
            columns = convert_format(connection.execute(text(SqlTemplate.columns_query.format(table_name=table_name))).fetchall())
            columns = [{**item, 'type': str(item['type'])} for item in columns]
            try:
                table_comment = table_convert_format(connection.execute(text(
                    SqlTemplate.table_comment_query.format(table_name=table_name, schema_name=schema_name.upper()))).fetchone())
            except Exception as e:
                table_comment = {}
            try:
                table_data_count = \
                    engine.connect().execute(text(
                        count_query.format(schema_name=schema_name.upper(), table_name=table_name.upper()))).fetchone()[
                        0]
            except Exception as e:
                table_data_count = None

            try:
                table_datastorge_count = \
                    engine.connect().execute(text(SqlTemplate.table_datastorge_query.format(schema_name=schema_name.upper(),
                                                                                table_name=table_name.upper()))).fetchone()[
                        0]
            except Exception as e:
                table_datastorge_count = None
            if not table_info:
                table_info = DbService.create_table(
                    session,
                    TableInfo,
                    datasource_id=datasource_id,
                    schedule_id=data.get('schedule_id'),
                    table_name=table_name,
                    data_total=table_data_count,
                    table_comment=table_comment.get('text'),
                    data_storage=table_datastorge_count
                )
                table_history_info = DbService.create_table(
                    session,
                    TableHistoryInfo,
                    datasource_id=datasource_id,
                    schedule_execute_id=schedule_execute.id,
                    table_name=table_name,
                    data_total=table_data_count,
                    table_comment=table_comment.get('text'),
                    data_storage=table_datastorge_count
                )
                table_info.table_history_id = table_history_info.id
            else:
                table_info.data_total = table_data_count
                table_info.table_comment = table_comment.get('text')
                table_info.update_time = int(datetime.now().timestamp())
                table_history_info = DbService.create_table(
                    session,
                    TableHistoryInfo,
                    datasource_id=datasource_id,
                    schedule_execute_id=schedule_execute.id,
                    table_name=table_name,
                    data_total=table_data_count,
                    table_comment=table_comment.get('text'),
                    table_history_id=table_info.table_history_id,
                    data_storage=table_datastorge_count
                )
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
                    DbService.create_table(
                        session,
                        FieldInfo,
                        table_info_id=table_info.id,
                        name=column.get('name'),
                        primary_keys=primary_keys,
                        type=column.get('type'),
                        nullable=column.get('nullable'),
                        default=column.get('default'),
                        autoincrement=column.get('autoincrement'),
                        comment=column.get('comment')
                    )
                else:
                    field_info.comment = column.get('comment')
                    field_info.type = column.get('type')
                    field_info.update_time = int(datetime.now().timestamp())
                DbService.create_table(
                    session,
                    FieldHistoryInfo,
                    table_info_id=table_history_info.id,
                    name=column.get('name'),
                    primary_keys=primary_keys,
                    type=column.get('type'),
                    nullable=column.get('nullable'),
                    default=column.get('default'),
                    autoincrement=column.get('autoincrement'),
                    comment=column.get('comment')
                )
            field_check_change(table_info.id, data, session)
        table_check_change(table_names, data, session)
        engine.dispose()


    @classmethod
    def dm_exploration(cls,database_address,username,password,database_name,datasource_id,data,schedule_execute,session):
        server = database_address.split(':')
        conn = dmPython.connect(user=username, password=password, server=server[0], port=server[1],
                                connection_timeout=30000, login_timeout=30000)
        cursor = conn.cursor()
        cursor.execute(
            f"select table_name, comments from dba_tab_comments where table_type='TABLE' and owner = '{database_name}'")
        tab_comments_list = cursor.fetchall()
        for table_name, table_comment in tab_comments_list:
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
                table_info = DbService.create_table(
                    session,
                    TableInfo,
                    datasource_id=datasource_id,
                    schedule_id=data.get('schedule_id'),
                    table_name=table_name,
                    data_total=data_total,
                    table_comment=table_comment
                )
                table_history_info = DbService.create_table(
                    session,
                    TableHistoryInfo,
                    datasource_id=datasource_id,
                    table_name=table_name,
                    data_total=data_total,
                    table_comment=table_comment,
                    schedule_execute_id=schedule_execute.id
                )
                table_info.table_history_id = table_history_info.id
            else:
                table_info.table_comment = table_comment
                table_info.data_total = data_total
                table_history_info = DbService.create_table(
                    session,
                    TableHistoryInfo,
                    datasource_id=datasource_id,
                    table_name=table_name,
                    data_total=data_total,
                    table_comment=table_comment,
                    schedule_execute_id=schedule_execute.id,
                    table_history_id=table_info.table_history_id
                )
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
                    DbService.create_table(
                        session,
                        FieldInfo,
                        table_info_id=table_info.id,
                        name=merged[1],
                        primary_keys=primary,
                        type=merged[2] + str(merged[3]),
                        nullable=nullable,
                        comment=merged[8]
                    )
                else:
                    field_info.type = merged[2] + str(merged[3])
                    field_info.nullable = nullable
                    field_info.comment = merged[8]
                DbService.create_table(
                    session,
                    FieldHistoryInfo,
                    table_info_id=table_history_info.id,
                    name=merged[1],
                    primary_keys=primary,
                    type=merged[2] + str(merged[3]),
                    nullable=nullable,
                    comment=merged[8]
                )
            field_check_change(table_info.id, data, session)
        table_check_change([table[0] for table in tab_comments_list], data, session)

if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.database.quality_result import QualityReportResult

    engine = create_engine('postgresql://root:123456@192.168.20.48:5432/bsp-user')
    session = sessionmaker(bind=engine)()
    record = DbService.create_table(
        session,
        QualityReportResult,
        database_id=1,
        quality_table_name='test'
    )
    DbService.update_record(
        session,
        record,
        quality_table_name='test1'
    )
    result = DbService.query_records(
    session,
    QualityReportResult,
        {"database_id": 1}
    )
    print(result)
