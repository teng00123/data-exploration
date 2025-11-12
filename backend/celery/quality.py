import statistics
from datetime import timedelta

from kombu.common import PREFETCH_COUNT_MAX

from backend.celery.sql.sql import SQLTemplate
from backend.celery.service import DbService
from backend.database.rule import Rule, RuleGroup
from backend.utils import decrypt_password
from backend.database.quality_result import QualityReportResult, QualityTimeliness, QualityIntegrity, \
    QualityRepeatability, QualityNormative, QualityNormativeDetail, QualityAccuracy, QualityConsistency
from backend.database.exploration_model import TableHistoryInfo, TableHistoryTemplateInfo, FieldHistoryInfo, TableInfo, \
    FieldInfo
from sqlalchemy import create_engine, text, desc
import urllib.parse


def empty_engine(database_info):
    # TODO: implement empty sql detection
    if database_info.get('database_type') == 'mysql':
        engine = create_engine(
            f'mysql+pymysql://{database_info.get("database_username")}:{urllib.parse.quote(decrypt_password(database_info.get("database_password")))}@{database_info.get("database_address")}/{database_info.get("database_name")}'
        )
        count_sql = SQLTemplate.COUNT_SQL
    elif database_info.get("database_type") == 'postgresql':
        engine = create_engine(
            f'postgresql+psycopg2://{database_info.get("database_username")}:{urllib.parse.quote(decrypt_password(database_info.get("database_password")))}@{database_info.get("database_address")}/{database_info.get("database_name")}'
        )
        count_sql = SQLTemplate.COUNT_SQL
    return engine, count_sql


def repetitive_engine(database_info):
    # TODO: implement empty sql detection
    if database_info.database_type == 'mysql':
        engine = create_engine(
            f'mysql+pymysql://{database_info.username}:{urllib.parse.quote(database_info.password)}@{database_info.host}:{database_info.port}/{database_info.database_name}'
        )
        count_sql = SQLTemplate.COUNT_SQL
    elif database_info.database_type == 'postgresql':
        engine = create_engine(
            f'postgresql+psycopg2://{database_info.username}:{urllib.parse.quote(database_info.password)}@{database_info.host}:{database_info.port}/{database_info.database_name}'
        )
        count_sql = SQLTemplate.COUNT_SQL
    return engine, count_sql


def sql_detection(
        session,
        _session,
        count_sql,
        table_name,
        table_id,
        field_name,
        comment,
        execute_id,
        database_id,
        rule_info
) -> tuple:
    """
    sql检测
    :param session: 本机系统数据库session
    :param _session: 质量检测数据库engine
    :param count_sql: 总数查询sql
    :param table_name: 表名
    :param field_name: 字段名
    :param execute_id:
    :param database_id:
    :param rule_info:
    :return:
    """
    group_rule_info = DbService.query_records(session, RuleGroup, filters={'id': rule_info.get('group_id')}, first=True)
    while group_rule_info.get('parent_id') is not None:
        group_rule_info = DbService.query_records(session, RuleGroup, filters={'id': group_rule_info.get('parent_id')}, first=True)
    if group_rule_info.get('group_name') == '数据完整性':
        result_model = QualityIntegrity
    elif group_rule_info.get('group_name') == '数据唯一性':
        result_model = QualityRepeatability
    elif group_rule_info.get('group_name') == '数据准确性':
        result_model = QualityAccuracy
    elif group_rule_info.get('group_name') == '数据一致性':
        result_model = QualityConsistency
    else:
        return True, f'group name not found!!!! {table_name}---result success'
    try:
        # TODO: implement empty score detection
        count_result = _session.execute(text(count_sql.format(table_name=table_name))).fetchall()[0][0]
        empty_result = _session.execute(text(rule_info.get('sql_expression').format(table_name=table_name, field_name=field_name))).fetchall()[0][
            0]
        if empty_result == 0:
            score = 0
        else:
            score = round(empty_result / count_result * rule_info.get('weight'), 2)
        DbService.create_table(session, result_model,
                               database_id=database_id, quality_table_name=table_name,
                               quality_field_name=field_name,
                               score=score, execute_id=execute_id,rule_id=rule_info.get('id'),table_id=table_id,count=count_result,problem_lines=count_result-empty_result)

        # 更新质量报告结果
    except Exception as e:
        _session.rollback()
        session.rollback()
        DbService.create_table(session, result_model,
                               database_id=database_id, quality_table_name=table_name,
                               quality_field_name=field_name, execute_id=execute_id,rule_id=rule_info.get('id'),execute_log=str(e),table_id=table_id)

        return False, f'sql detection failed for table {table_name}---error {e}'
    finally:
        session.close()
        _session.close()
    return True, f'sql detection completed for table {table_name}---result success'

def re_detection(
        session,
        _session,
        count_sql,
        table_name,
        table_id,
        field_name,
        comment,
        execute_id,
        database_id,
        rule_info
) -> tuple:
    """
    正则检测
    :param session: 本机系统数据库session
    :param _session: 质量检测数据库engine
    :param count_sql: 总数查询sql
    :param table_name: 表名
    :param field_name: 字段名
    :param execute_id:
    :param database_id:
    :param rule_info:
    """
    group_rule_info = DbService.query_records(session, RuleGroup, filters={'id': rule_info.get('group_id')}, first=True)
    while group_rule_info.get('parent_id') is not None:
        group_rule_info = DbService.query_records(session, RuleGroup, filters={'id': group_rule_info.get('parent_id')},
                                                  first=True)
    if group_rule_info.get('group_name') == '数据完整性':
        result_model = QualityIntegrity
    elif group_rule_info.get('group_name') == '数据唯一性':
        result_model = QualityRepeatability
    elif group_rule_info.get('group_name') == '数据准确性':
        result_model = QualityAccuracy
    elif group_rule_info.get('group_name') == '数据一致性':
        result_model = QualityConsistency
    else:
        return True, f're detection completed for table {table_name}---result success'
    try:
        # TODO: implement empty score detection
        count_result = _session.execute(text(count_sql.format(table_name=table_name))).fetchall()[0][0]
        empty_result = _session.execute(text(f"SELECT COUNT(1) FROM {table_name} WHERE {field_name} ~ :regex"),{'regex':rule_info.get('re_expression')}).fetchall()[0][0]
        if empty_result == 0:
            score = 0
        else:
            score = round(empty_result / count_result * rule_info.get('weight'), 2)
        DbService.create_table(session, result_model,
                               database_id=database_id, quality_table_name=table_name,
                               quality_field_name=field_name,
                               score=score, execute_id=execute_id, rule_id=rule_info.get('id'),table_id=table_id)

        # 更新质量报告结果
    except Exception as e:
        _session.rollback()
        session.rollback()
        DbService.create_table(session, result_model,
                               database_id=database_id, quality_table_name=table_name,
                               quality_field_name=field_name, execute_id=execute_id, rule_id=rule_info.get('id'),
                               execute_log=str(e),table_id=table_id)
        return False, f're_detection failed for table {table_name}---error {e}'
    finally:
        _session.close()
        session.close()
    return True, f're_detection completed for table {table_name}---result success'

def timeliness_score_detection(
        session,
        table_name,
        database_id,
        execute_id,
        up_cycle
):
    try:
        table_history_info = DbService.query_records(session, TableInfo,
                                                     filters={"datasource_id": database_id, "table_name": table_name},
                                                     order_by='-create_time', first=True)
        if up_cycle == '每日':
            create_time = int(table_history_info.get('create_time')) - 86460
        elif up_cycle == '每月':
            create_time = int(table_history_info.get('create_time')) - 2592060
        elif up_cycle == '每年':
            create_time = int(table_history_info.get('create_time')) - 31536060
        else:
            create_time = int(table_history_info.get('create_time'))
        time_interval = [str(i) for i in range(create_time, int(table_history_info.get('create_time')))]
        table_history_info = session.query(TableInfo).filter_by(datasource_id=database_id,table_name=table_name).filter(TableInfo.create_time.in_(time_interval)).all()
        timeliness = 0
        if len(table_history_info) == 0:
            data_total = 0
        else:
            data_total = table_history_info[0].data_total
        for table_info in table_history_info:
            if table_info.data_total != data_total:
                timeliness = 1
        DbService.create_table(
            session,
            QualityTimeliness,
            database_id=database_id, quality_table_name=table_name,
            timeliness=timeliness, execute_id=execute_id,result='success', commit=True)
    except Exception as e:
        DbService.create_table(
            session,
            QualityTimeliness,
            database_id=database_id, quality_table_name=table_name, execute_id=execute_id,result=e, commit=True)
        return False, f'Timeliness score detection failed for table {table_name}---error {e}'
    finally:
        session.close()
    return True, f'Timeliness score detection completed for table {table_name}---success'

def generate_report_detection(
        session,
        database_id,
        execute_id
):
    try:
        latest_quality_integrity = DbService.query_records(session, QualityIntegrity, {"database_id": database_id, "execute_id": execute_id,'execute_log': None})
        latest_quality_repeatability = DbService.query_records(session, QualityRepeatability, {"database_id": database_id, "execute_id": execute_id,'execute_log': None})
        latest_quality_accuracy = DbService.query_records(session, QualityAccuracy, {"database_id": database_id, "execute_id": execute_id,'execute_log': None})
        latest_quality_consistency = DbService.query_records(session, QualityConsistency, {"database_id": database_id, "execute_id": execute_id,'execute_log': None})
        table_dict = dict()
        for table_info in latest_quality_integrity:
            if table_dict.get(table_info.get('quality_table_name')) is None:
                table_dict[table_info.get('quality_table_name')] = dict()
                table_dict[table_info.get('quality_table_name')]['id'] = table_info.get('table_id')
            rule_info = DbService.query_records(session, Rule, {"id": table_info.get('rule_id')}, first=True)
            if table_dict[table_info.get('quality_table_name')].get('integrity') is None:
                table_dict[table_info.get('quality_table_name')]['integrity'] = table_info.get('score')
            else:
                table_dict[table_info.get('quality_table_name')]['integrity'] += table_info.get('score')
            if table_dict[table_info.get('quality_table_name')].get('integrity_weight') is None:
                table_dict[table_info.get('quality_table_name')]['integrity_weight'] = rule_info.get('weight')
            else:
                table_dict[table_info.get('quality_table_name')]['integrity_weight'] += rule_info.get('weight')
        for table_info in latest_quality_repeatability:
            if table_dict.get(table_info.get('quality_table_name')) is None:
                table_dict[table_info.get('quality_table_name')] = dict()
                table_dict[table_info.get('quality_table_name')]['id'] = table_info.get('table_id')
            rule_info = DbService.query_records(session, Rule, {"id": table_info.get('rule_id')}, first=True)
            if table_dict[table_info.get('quality_table_name')].get('repeatability') is None:
                table_dict[table_info.get('quality_table_name')]['repeatability'] = table_info.get('score')
            else:
                table_dict[table_info.get('quality_table_name')]['repeatability'] += table_info.get('score')
            if table_dict[table_info.get('quality_table_name')].get('repeatability_weight') is None:
                table_dict[table_info.get('quality_table_name')]['repeatability_weight'] = rule_info.get('weight')
            else:
                table_dict[table_info.get('quality_table_name')]['repeatability_weight'] += rule_info.get('weight')
        for table_info in latest_quality_accuracy:
            if table_dict.get(table_info.get('quality_table_name')) is None:
                table_dict[table_info.get('quality_table_name')] = dict()
                table_dict[table_info.get('quality_table_name')]['id'] = table_info.get('table_id')
            rule_info = DbService.query_records(session, Rule, {"id": table_info.get('rule_id')}, first=True)
            if table_dict[table_info.get('quality_table_name')].get('accuracy') is None:
                table_dict[table_info.get('quality_table_name')]['accuracy'] = table_info.get('score')
            else:
                table_dict[table_info.get('quality_table_name')]['accuracy'] += table_info.get('score')
            if table_dict[table_info.get('quality_table_name')].get('accuracy_weight') is None:
                table_dict[table_info.get('quality_table_name')]['accuracy_weight'] = rule_info.get('weight')
            else:
                table_dict[table_info.get('quality_table_name')]['accuracy_weight'] += rule_info.get('weight')
        for table_info in latest_quality_consistency:
            if table_dict.get(table_info.get('quality_table_name')) is None:
                table_dict[table_info.get('quality_table_name')] = dict()
                table_dict[table_info.get('quality_table_name')]['id'] = table_info.get('table_id')
            rule_info = DbService.query_records(session, Rule, {"id": table_info.get('rule_id')}, first=True)
            if table_dict[table_info.get('quality_table_name')].get('consistency') is None:
                table_dict[table_info.get('quality_table_name')]['consistency'] = table_info.get('score')
            else:
                table_dict[table_info.get('quality_table_name')]['consistency'] += table_info.get('score')
            if table_dict[table_info.get('quality_table_name')].get('consistency_weight') is None:
                table_dict[table_info.get('quality_table_name')]['consistency_weight'] = rule_info.get('weight')
            else:
                table_dict[table_info.get('quality_table_name')]['consistency_weight'] += rule_info.get('weight')
        for table_name in table_dict.keys():
            check_num = 4
            repeatability = table_dict.get(table_name).get('repeatability')
            if repeatability is None:
                check_num -= 1
            integrity = table_dict.get(table_name).get('integrity')
            if integrity is None:
                check_num -= 1
            accuracy = table_dict.get(table_name).get('accuracy')
            if accuracy is None:
                check_num -= 1
            consistency = table_dict.get(table_name).get('consistency')
            if consistency is None:
                check_num -= 1
            repeatability_weight = 0 if table_dict.get(table_name).get('repeatability_weight') is None else table_dict.get(table_name).get('repeatability_weight')
            integrity_weight = 0 if table_dict.get(table_name).get('integrity_weight') is None else table_dict.get(table_name).get('integrity_weight')
            accuracy_weight = 0 if table_dict.get(table_name).get('accuracy_weight') is None else table_dict.get(table_name).get('accuracy_weight')
            consistency_weight = 0 if table_dict.get(table_name).get('consistency_weight') is None else table_dict.get(table_name).get('consistency_weight')
            table_weight = repeatability_weight + integrity_weight + accuracy_weight + consistency_weight
            table_integrity = None if integrity is None else round(integrity / (integrity_weight / 25), 2)
            table_accuracy = None if accuracy is None else round(accuracy / (accuracy_weight / 25), 2)
            table_consistency = None if consistency is None else round(consistency / (consistency_weight / 25), 2)
            table_repeatability = None if repeatability is None else round(repeatability / (repeatability_weight / 25), 2)
            total = sum((value / 25) * (100 / check_num)  if value is not None else 0 for value in [table_repeatability, table_integrity, table_accuracy, table_consistency])
            DbService.create_table(
                session,
                QualityReportResult,
                execute_id=execute_id,
                database_id=database_id,
                quality_table_name=table_name,
                repeatability=table_repeatability,
                integrity=table_integrity,
                accuracy=table_accuracy,
                consistency=table_consistency,
                total=round(total, 2),
                table_id=table_dict.get(table_name).get('id'),
                commit=True
            )
            table_dict[table_name]['table_integrity'] = table_integrity
            table_dict[table_name]['table_accuracy'] = table_accuracy
            table_dict[table_name]['table_consistency'] = table_consistency
            table_dict[table_name]['table_repeatability'] = table_repeatability
            table_dict[table_name]['total'] = total
            table_dict[table_name]['weight'] = table_weight
        a = [table_dict.get(i).get('table_integrity')  for i in table_dict.keys() if table_dict.get(i).get('table_integrity') is not None]
        b = [table_dict.get(i).get('table_repeatability')  for i in table_dict.keys() if table_dict.get(i).get('table_repeatability') is not None]
        c = [table_dict.get(i).get('table_accuracy')  for i in table_dict.keys() if table_dict.get(i).get('table_accuracy') is not None]
        d = [table_dict.get(i).get('table_consistency')  for i in table_dict.keys() if table_dict.get(i).get('table_consistency') is not None]
        total_integrity = round(statistics.mean(a),2) if len(a) > 0 else None
        total_repeatability = round(statistics.mean(b),2) if len(b) > 0 else None
        total_accuracy = round(statistics.mean(c),2) if len(c) > 0 else None
        total_consistency = round(statistics.mean(d),2) if len(d) > 0 else None
        all_values = [total_integrity, total_repeatability, total_accuracy, total_consistency]
        valid_values = [v for v in all_values if v is not None]
        if len(valid_values) > 0:
            final_average = sum(valid_values)
        else:
            final_average = None  # 或者 0，取决于你的业务逻辑
        total = round(final_average * 4 / len(valid_values), 2)

        DbService.create_table(
            session,
            QualityReportResult,
            database_id=database_id, execute_id=execute_id, repeatability=total_repeatability, integrity=total_integrity,accuracy=total_accuracy,consistency=total_consistency, total=total, commit=True)

    except Exception as e:
        session.rollback()
        return False, f'generate report detection failed for database {database_id}---error {e}'
    finally:
        session.close()
    return True, f'generate report detection completed for table {database_id}---success'


def normative_detection(
        session,
        table_id,
        execute_id
):
    try:
        table_info = DbService.query_records(session, TableInfo, {"id": table_id}, first=True)
        if table_info.get('table_comment') is None or table_info.get('table_comment') == '':
            table_no_comment = 1
        else:
            table_no_comment = 0
        field_infos = DbService.query_records(session, FieldInfo, {"table_info_id": table_id})
        field_no_comment = 0
        primary_keys = False
        for field_info in field_infos:
            if field_info.get('comment') is None or field_info.get('comment') == '':
                field_no_comment += 1
            if field_info.get('primary_keys') is True:
                primary_keys = True
            DbService.create_table(
                session,
                QualityNormativeDetail,
                execute_id=execute_id,
                database_id=table_info.get('datasource_id'),
                quality_table_id=table_id,
                quality_field_id=field_info.get('id'),
                field_name=field_info.get('name'),
                field_comment=field_info.get('comment'),
                field_type=field_info.get('type'),
                is_primary_key=field_info.get('primary_keys'),
                commit=True
            )
        DbService.create_table(
            session,
            QualityNormative,
            execute_id=execute_id,
            database_id=table_info.get('datasource_id'),
            quality_table_id=table_id,
            table_no_comment=table_no_comment,
            field_no_comment=field_no_comment,
            is_have_primary_keys=primary_keys,
            field_count = len(field_infos),
            commit=True
        )
    except Exception as e:
        return False, f'Normative score detection failed for table {table_id}---error {e}'
    finally:
        session.close()
    return True, f'Normative score detection completed for table {table_id}---success'
