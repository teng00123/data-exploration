# tasks.py
import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(__file__)

# 获取上两层的目录
two_levels_up = os.path.dirname(os.path.dirname(current_dir))

# 将上两层的目录添加到sys.path
sys.path.append(two_levels_up)
from datetime import datetime, timedelta

from backend.database.management import VariableManageInfo
from backend.database.rule import Rule, ConfigureRuleInfo, ConfigureTimelinessInfo, RuleGroup
from backend.database.quality_result import QualityExecute, QualityReportResult, QualityIntegrity, QualityRepeatability, \
    QualityAccuracy, QualityConsistency, QualityNormative, QualityNormativeDetail, QualityTimeliness
from backend.database.exploration_model import DatasourceInfo, BelongSystem
from backend.celery.quality import (sql_detection, empty_engine, normative_detection, timeliness_score_detection,re_detection,
                                    generate_report_detection)
from backend.database.exploration_model import TableInfo, FieldInfo
from backend.celery.service import DbService
from backend.config import config
from backend.database.log import SendSMSLog
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

import urllib.parse
from celery import Celery
import random
import logging

from backend.database.sys_model import SysDept
from backend.service.v1_service import ReportGenerateService
from backend.service.sms_service import CommonPlatformShortMessageService

# 1. 创建 Celery 应用实例
#    通常使用项目名称作为命名空间，避免冲突
celery_app = Celery('distributed_task_demo')

# 2. 配置 Celery
#    使用环境变量或配置文件是更好的做法，这里为了简单直接写死
if config.get('redis').get('is_password') == False:
    redis_url = f'redis://@{config.get("redis").get("host")}:{config.get("redis").get("port")}'
else:
    redis_url = f'redis://:{config.get("redis").get("password")}@{config.get("redis").get("host")}:{config.get("redis").get("port")}'

celery_app.conf.update(
    # 2.1 消息代理 (Broker): Celery 用于发送/接收任务消息
    broker_url=f'{redis_url}/0',  # 连接到本地的 Redis，数据库 0

    # 2.2 结果后端 (Backend): Celery 用于存储任务状态和结果
    result_backend=f'{redis_url}/1',  # 使用 Redis 的另一个数据库 (1) 存储结果
    # beat_max_loop_interval=beat_max_loop_interval,
    # beat_dburi=beat_dburi,
    # worker_max_tasks_per_child= worker_max_tasks_per_child,
    # 2.4 (可选) 任务序列化格式，推荐 JSON
    task_serializer='json',
    accept_content=['json'],  # 只接受 JSON 格式的任务
    result_serializer='json',
    # timezone=timezone,
    enable_utc=True
)

# 设置日志 (可选，但推荐)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def create_task(self, datasource_id, table_id):
    task_id = self.request.id  # 获取当前任务的唯一 ID
    id = random.randint(1, 1000000000000)
    logger.info(f"Task {task_id} started: create task")
    # TODO: implement task creation logic
    engine = create_engine(
        f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    session = sessionmaker(bind=engine)()
    datasource_info = DbService.query_records(session, DatasourceInfo, filters={"id": datasource_id}, first=True)
    DbService.create_table(session, QualityExecute, id=id,schedule_name=datasource_info.get('datasource_name') + '规则检测', database_id=datasource_id,
                           quality_table_id=table_id, rule_type='规则检查',
                           execute_status='执行中',
                           execute_time=datetime.utcnow())
    _engine,count_sql = empty_engine(datasource_info)
    _session = sessionmaker(bind=_engine)()
    try:
        configure_rule_info = DbService.query_records(session, ConfigureRuleInfo, filters={"datasource_id":datasource_id})
        # 单个字段配置规则
        for configure_rule in configure_rule_info:
            rule_id = configure_rule.get('rule_id')
            rule = DbService.query_records(session, Rule, filters={"id": rule_id}, first=True)
            if rule is None:
                logger.info('rule is None')
            else:
                table_info = DbService.query_records(session,TableInfo,filters={'id': configure_rule.get('table_id')},first=True)
                if rule.get('expression') == 'sql规则配置' and rule.get('is_timeliness') is False:
                    if rule.get('dimension') == 'field':
                        field_info = DbService.query_records(session, FieldInfo, filters={"table_info_id": table_info.get('id'), "id": configure_rule.get('field_id')}, first=True)
                        comment = field_info.get('name') if field_info.get('comment') is None else field_info.get('comment')
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
                    logger.info(text)
                else:
                    if rule.get('dimension') == 'field':
                        field_info = DbService.query_records(session, FieldInfo, filters={"table_info_id": table_info.get('id'), "id": configure_rule.get('field_id')}, first=True)
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
                                                 table_info.get('table_name'),table_info.get('id'),
                                                 field_name,comment, id, datasource_id, rule)
                    logger.info(text)
        # 规范性检查
        table_infos = DbService.query_records(session, TableInfo,filters={"datasource_id": datasource_id})
        for table_info in table_infos:
            status, text = normative_detection(session, table_info.get('id'),id)
            logger.info(text)
            configure_timeliness = DbService.query_records(session,ConfigureTimelinessInfo,filters={"table_id": table_info.get('id')}, first=True)
            # 时效性检查
            status, text = timeliness_score_detection(session, table_info.get('table_name'), datasource_id,id,configure_timeliness.get('timeliness'))
            logger.info(text)
        status, text = generate_report_detection(session, datasource_id, id)
        logger.info(text)
        status, text = create_pdf(session, datasource_id,id)
        logger.info(text)
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
    return f"create Task {task_id} created"

def create_pdf(session,datasource_id,execute_id):
    file_name = str(execute_id) + str(datasource_id) + '.pdf'
    datasource_info = DbService.query_records(session,DatasourceInfo,filters={'id':datasource_id},first=True)
    dept_info = DbService.query_records(session,SysDept,filters={'dept_id':datasource_info.get('belonging_system_department_id')},first=True)
    quality_result = DbService.query_records(session,QualityReportResult,filters={'execute_id':execute_id,'table_id':None},first=True)
    configure_rule_info = DbService.query_records(session,ConfigureRuleInfo,filters={'datasource_id':datasource_id})
    quality_accuracy = DbService.query_records(session,QualityAccuracy,filters={'database_id': datasource_id, 'execute_id': execute_id},
                                                filter=QualityAccuracy.table_id is not None)
    quality_consistency = DbService.query_records(session,QualityConsistency,filters={'database_id': datasource_id, 'execute_id': execute_id},
                                                filter=QualityConsistency.table_id is not None)
    quality_repeatability = DbService.query_records(session,QualityRepeatability,filters={'database_id': datasource_id, 'execute_id': execute_id},
                                                filter=QualityRepeatability.table_id is not None)
    quality_integrity = DbService.query_records(session,QualityIntegrity,filters={'database_id': datasource_id, 'execute_id': execute_id},
                                                filter=QualityIntegrity.table_id is not None)
    normative_info = DbService.query_records(session,QualityNormative,filters={'execute_id':execute_id,'database_id':datasource_id})
    timeliness_info = DbService.query_records(session,QualityTimeliness,filters={'execute_id':execute_id,'database_id':datasource_id})

    quality_result_data = quality_integrity + quality_repeatability + quality_consistency + quality_accuracy

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    random_number = ''.join(str(random.randint(0, 9)))
    report_code = timestamp + random_number
    check_date = datetime.now().strftime('%Y-%m-%d')
    database_name = datasource_info.get('database_name')
    ip = datasource_info.get('database_address').split(':')[0]
    success_rule_count = len(configure_rule_info)
    field_set = set()
    table_set = set()
    rule_dict = dict()
    data_total = 0
    field_table_data3 = {}
    field_table_data3_list = []
    field_table_data2 = [quality_result.get('integrity'),quality_result.get('consistency'),quality_result.get('accuracy'),quality_result.get('repeatability')]
    field_table_data = {}
    field_table_data_list = {
        'integrity': [],
         'consistency': [],
         'accuracy': [],
         'repeatability': []
    }
    problem_details = []
    normative_data = []
    timeless_data = []
    rule_set = set()
    field_table_data3_integrity = 0
    field_table_data3_consistency = 0
    field_table_data3_accuracy = 0
    field_table_data3_repeatability = 0
    for configure_rule in configure_rule_info:
        rule_info = DbService.query_records(session,Rule,filters={'id':configure_rule.get('rule_id')},first=True)
        if configure_rule.get('field_id') is not None:
            field_set.add(configure_rule.get('field_id'))
        if rule_info.get('is_timeliness') is True:
            success_rule_count -= 1
            continue
        if configure_rule.get('rule_id') not in rule_set:
            group_name = get_rule_group_name(rule_info, session)
            if group_name == '数据完整性':
                field_table_data3_integrity += 1
            elif group_name == '数据一致性':
                field_table_data3_consistency += 1
            elif group_name == '数据准确性':
                field_table_data3_accuracy += 1
            elif group_name == '数据唯一性':
                field_table_data3_repeatability += 1
            field_table_data3_list.append([group_name,rule_info.get('rule_type'),rule_info.get('rule_code'),rule_info.get('describe'),rule_info.get('refer_text'),
                                           rule_info.get('question_level'),str(rule_info.get('weight'))])
        rule_dict[rule_info.get('id')]= rule_info
        table_set.add(configure_rule.get('table_id'))
        rule_set.add(configure_rule.get('rule_id'))
    field_table_data3['integrity'] = field_table_data3_integrity
    field_table_data3['consistency'] = field_table_data3_consistency
    field_table_data3['accuracy'] = field_table_data3_accuracy
    field_table_data3['repeatability'] = field_table_data3_repeatability
    field_table_data3['data'] = field_table_data3_list
    problem_details_integrity = 0
    problem_details_consistency = 0
    problem_details_accuracy = 0
    problem_details_repeatability = 0
    for item in quality_result_data:
        if item.get('execute_log'):
            success_rule_count -= 1
            continue
        data_total += item.get('count')
        rule_info = rule_dict.get(item.get('rule_id'))
        field_name = item.get('quality_field_name')
        group_name = get_rule_group_name(rule_info, session)
        if rule_info.get('dimension') == 'table':
            field_name = ''
        proportion = str(round(item.get('problem_lines')/ item.get('count')*100,2)) if item.get('count') != 0 else '0'
        if group_name == '数据完整性':
            field_table_data_list.get('integrity').append(
                [group_name,rule_info.get('rule_type'),rule_info.get('rule_code'),rule_info.get('describe'),rule_info.get('question_level'),str(rule_info.get('weight'))
                    ,item.get('quality_table_name'),field_name,
                 str(item.get('problem_lines')),proportion,str(item.get('score'))
                 ])
        elif group_name == '数据一致性':
            field_table_data_list.get('consistency').append(
                [group_name,rule_info.get('rule_type'),rule_info.get('rule_code'),rule_info.get('describe'),rule_info.get('question_level'),str(rule_info.get('weight'))
                    ,item.get('quality_table_name'),field_name,
                 str(item.get('problem_lines')),proportion,str(item.get('score'))
                 ])
        elif group_name == '数据准确性':
            field_table_data_list.get('accuracy').append(
                [group_name, rule_info.get('rule_type'), rule_info.get('rule_code'), rule_info.get('describe'),
                 rule_info.get('question_level'), str(rule_info.get('weight'))
                    , item.get('quality_table_name'), field_name,
                 str(item.get('problem_lines')), proportion, str(item.get('score'))
                 ])
        elif group_name == '数据唯一性':
            field_table_data_list.get('repeatability').append(
                [group_name, rule_info.get('rule_type'), rule_info.get('rule_code'), rule_info.get('describe'),
                 rule_info.get('question_level'), str(rule_info.get('weight'))
                    , item.get('quality_table_name'), field_name,
                 str(item.get('problem_lines')), proportion, str(item.get('score'))
                 ])
        reason = rule_info.get('rule_code') + "规则，检测未通过"
        if item.get('count') == 0 and item.get('problem_lines') == 0:
            reason = '无数据'
        elif item.get('count') != 0 and item.get('problem_lines') == 0:
            continue
        if group_name == '数据完整性':
            problem_details_integrity += 1
        elif group_name == '数据一致性':
            problem_details_consistency += 1
        elif group_name == '数据准确性':
            problem_details_accuracy += 1
        elif group_name == '数据唯一性':
            problem_details_repeatability += 1
        problem_details.append(
            {
                'name':group_name,
                'data':[
                    ['表名',item.get('quality_table_name')],
                    ['字段名',field_name],
                    ['原因', reason],
                    ['问题数据行数',str(item.get('problem_lines'))],
                    ['影响范围','']
                ]
            }
        )
    field_table_data['integrity'] = problem_details_integrity
    field_table_data['consistency'] = problem_details_consistency
    field_table_data['accuracy'] = problem_details_accuracy
    field_table_data['repeatability'] = problem_details_repeatability
    field_table_data['data'] = field_table_data_list
    normative_status = '合格'
    for normative in normative_info:
        if normative.get('table_no_comment') > 0 or normative.get('field_no_comment') > 0 or normative.get('is_have_primary_keys') is False:
            normative_status = '不合格'
        table_info = DbService.query_records(session,TableInfo,filters={'id':normative.get('quality_table_id')},first=True)
        normative_dict = {
            'table_name':table_info.get('table_name'),
            'is_table_comment': '否' if normative.get('table_no_comment') == 1 else '是',
            'normative_field_count': normative.get('field_count'),
            'field_no_comment': normative.get('field_no_comment'),
            'is_pk': '否' if normative.get('is_have_primary_keys') is False  else '是',
            'data':[]
        }
        normative_details = DbService.query_records(session,QualityNormativeDetail,filters={'execute_id':execute_id,'database_id':datasource_id,'quality_table_id':normative.get('quality_table_id')})
        for normative_details_item in normative_details:
            normative_dict['data'].append([table_info.get('table_name'),normative_details_item.get('field_name'),normative_details_item.get('field_type')
                                              ,'' if normative_details_item.get('field_comment') is None else normative_details_item.get('field_comment')
                                              ,'否' if normative_details_item.get('is_primary_key') is False else '是'])
        normative_data.append(normative_dict)
    timeless_status = '合格'
    for timeless in timeliness_info:
        if timeless.get('timeliness') == 0:
            timeless_status = '不合格'
        timeless_data.append([timeless.get('quality_table_name'),'合格' if timeless.get('timeliness') == 1 else '不合格'])
    dept_name = dept_info.get('dept_name')
    check_score = DbService.query_records(session,VariableManageInfo,filters={'variable_name':'check_score'},first=True)
    check_total = quality_result.get('total')
    rule_total = len(configure_rule_info)
    field_count = len(field_set)
    table_count = len(table_set)
    check_status = '合格' if check_total > int(check_score.get('variable_value')) else '不合格'
    report_service = ReportGenerateService()
    try:
        report_service.create_pdf(
            file_name=file_name,
            database_name=database_name,
            dept_name=dept_name,
            ip=ip,
            report_code=report_code,
            check_date=check_date,
            check_status=check_status,
            check_total=check_total,
            data_total=data_total,
            field_count=field_count,
            rule_total=rule_total,
            table_count=table_count,
            field_table_data=field_table_data,
            field_table_data2=field_table_data2,
            field_table_data3=field_table_data3,
            problem_details=problem_details,
            success_rule_count=success_rule_count,
            normative_data=normative_data,
            timeless_data=timeless_data,
            normative_status=normative_status,
            timeless_status=timeless_status
        )
        if check_status == '不合格':
            system_info = DbService.query_records(session, BelongSystem,
                                                  filters={'id': datasource_info.get('belonging_system_id')},
                                                  first=True)
            content = [f'{datasource_info.get("datasource_name")}/{system_info.get("system_name")}',
                        f'{table_count}',f'{field_count/10000}', f'{len(problem_details)}',f'{check_total}','数据探查系统','刘洋'
                       ]
            sms_content = f"""
            您好，关于【{datasource_info.get("datasource_name")}/{system_info.get("system_name")}】的数据质量探查已完成。探查期间共涉及【{table_count}】张表，【{field_count/10000}】万条数据，整体数据质量良好/存在【{len(problem_details)}】处异常。整体得分【{check_total}】，为不合格状态，详细报告已发送至【数据探查系统】，请查收。如有疑问，请联系【刘洋】。谢谢！
            """
            status = send_sms_message(mobile=system_info.get('phone'), content=content)
            DbService.create_table(session,SendSMSLog,user_id=system_info.get('create_id'),nick_name=system_info.get('person'),phone=system_info.get('phone'),
                                   department=system_info.get('department'),belonging_department=system_info.get('belonging_department'),sms_type='评分不达标',
                                   send_status='成功' if status is True else '失败',sms_content=sms_content)
    except Exception as e:
        logger.info('error'+str(e))
        return False, '生成报告失败', check_total > int(check_score.get('variable_value'))
    return True,f'生成报告{file_name}成功'


def get_rule_group_name(data,session):
    group_info = DbService.query_records(session,RuleGroup,filters={'id':data.get('group_id')},first=True)
    while True:
        group_info = DbService.query_records(session,RuleGroup,filters={'id':group_info.get('parent_id')},first=True)
        if group_info.get('parent_id') is None:
            break
    return group_info.get('group_name')

def send_sms_message(
        mobile: str='',
        template_id: int=1,
        content: list=[]
):
    sms_config = config.get('sms_config')
    service = CommonPlatformShortMessageService(sms_config)
    status = service.send_short_message(mobile, template_id, content)
    return status