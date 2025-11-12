# tasks.py
from datetime import datetime, timedelta

from backend.celery.tasks import create_pdf
from backend.database.rule import Rule, ConfigureRuleInfo
from backend.database.quality_result import QualityExecute
from backend.database.exploration_model import DatasourceInfo
from backend.celery.quality import (sql_detection, empty_engine, normative_detection, timeliness_score_detection,re_detection,
                                    generate_report_detection)
from backend.database.exploration_model import TableInfo, FieldInfo
from backend.celery.service import DbService
from backend.config import config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

import urllib.parse
import random


def schedule_create_task(data):
    print(f"Task schedule_create_task started: {data}")
    # TODO: implement task creation logic
    create_task(data.get('datasource_id'), data.get('table_id'))
    print(f"Task schedule_create_task finished: {data}")
    return f"Task schedule_create_task finished: {data}"


def create_task(datasource_id, table_id):
    id = random.randint(1, 1000000000000)
    # TODO: implement task creation logic
    engine = create_engine(
        f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    session = sessionmaker(bind=engine)()
    datasource_info = DbService.query_records(session, DatasourceInfo, filters={"id": datasource_id}, first=True)
    DbService.create_table(session, QualityExecute, id=id,
                           schedule_name=datasource_info.get('datasource_name') + '规则检测', database_id=datasource_id,
                           quality_table_id=table_id, rule_type='规则检查',
                           execute_status='执行中',
                           execute_time=datetime.utcnow())
    _engine, count_sql = empty_engine(datasource_info)
    _session = sessionmaker(bind=_engine)()
    try:
        configure_rule_info = DbService.query_records(session, ConfigureRuleInfo,
                                                      filters={"datasource_id": datasource_id})
        # 单个字段配置规则
        for configure_rule in configure_rule_info:
            rule_id = configure_rule.get('rule_id')
            rule = DbService.query_records(session, Rule, filters={"id": rule_id}, first=True)
            if rule is None:
                continue
            table_info = DbService.query_records(session, TableInfo,
                                                 filters={'id': configure_rule.get('table_id')}, first=True)
            if rule.get('expression') == 'sql规则配置' and rule.get('is_timeliness') is False:
                if rule.get('dimension') == 'field':
                    field_info = DbService.query_records(session, FieldInfo,
                                                         filters={"table_info_id": table_info.get('id'),
                                                                  "id": configure_rule.get('field_id')}, first=True)
                    comment = field_info.get('name') if field_info.get('comment') is None else field_info.get(
                        'comment')
                    field_name = field_info.get('name')
                else:
                    field_info = DbService.query_records(session, FieldInfo,
                                                         filters={"table_info_id": table_info.get('id')})
                    comment = ','.join([
                        i.get('comment') if i.get('comment') is not None else i.get('name')
                        for i in field_info if i.get('primary_keys') != True
                    ])
                    field_name = ','.join([i.get('name') for i in field_info if i.get('primary_keys') != True])
                status, text = sql_detection(session, _session, count_sql,
                                             table_info.get('table_name'), table_info.get('id'),
                                             field_name, comment, id, datasource_id, rule)
            else:
                if rule.get('dimension') == 'field':
                    field_info = DbService.query_records(session, FieldInfo,
                                                         filters={"table_info_id": table_info.get('id'),
                                                                  "id": configure_rule.get('field_id')}, first=True)
                    comment = field_info.get('name') if field_info.get('comment') is None else field_info.get(
                        'comment')
                    field_name = field_info.get('name')
                else:
                    field_info = DbService.query_records(session, FieldInfo,
                                                         filters={"table_info_id": table_info.get('id')})
                    field_name = ','.join([i.get('name') for i in field_info if i.get('primary_keys') != True])
                    comment = ','.join([
                        i.get('comment') if i.get('comment') is not None else i.get('name')
                        for i in field_info if i.get('primary_keys') != True
                    ])
                status, text = re_detection(session, _session, count_sql,
                                            table_info.get('table_name'), table_info.get('id'),
                                            field_name, comment, id, datasource_id, rule)
        # 规范性检查
        table_infos = DbService.query_records(session, TableInfo,
                                              filters={"datasource_id": datasource_id})
        for table_info in table_infos:
            status, text = normative_detection(session, table_info.get('id'), id)
            # 时效性检查
            status, text = timeliness_score_detection(session, table_info.get('table_name'), datasource_id, id, '每日')
        status, text = generate_report_detection(session, datasource_id, id)
        status, text = create_pdf(session, datasource_id, id)
        quality_execute_info = session.query(QualityExecute).filter_by(id=id).first()
        quality_execute_info.execute_status = '执行成功'
        quality_execute_info.execute_time = datetime.utcnow()
    except Exception as e:
        session.rollback()
        quality_execute_info = session.query(QualityExecute).filter_by(id=id).first()
        quality_execute_info.execute_status = '执行失败'
        quality_execute_info.execute_result = str(e)
        quality_execute_info.execute_time = datetime.utcnow()
    finally:
        session.commit()
        session.close()
        _session.close()
    return f"create Task created"
