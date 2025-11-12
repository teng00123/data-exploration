import base64
import json
import os.path
import random
import time

from flask import Blueprint, request
from backend.database.base import GenericCRUD
from backend.database.rule import RuleGroup, RuleGroupGraph, Rule, RuleGraph, ConfigureRuleInfo, ConfigureRuleFieldInfo, \
    ConfigureRuleTableInfo, ConfigureTimelinessInfo
from backend.database.exploration_model import DatasourceInfo, TableHistoryTemplateInfo, FieldHistoryInfo, FieldInfo, \
    TableInfo, BelongSystem
from backend.database.quality_result import QualityExecute, QualityReportResult, QualityIntegrity, QualityRepeatability, \
    QualityTimeliness, QualityNormative, QualityNormativeDetail, QualityAccuracy, QualityConsistency
from backend.database.quality_inspection import QualitySchedulerInfo
from backend.config import r, config
from backend.response.code import SuccessResponse, ErrorResponse, FileResponse, StreamResponse
from backend.utils import Pagination, record_user_operation, is_sql_injection_risky, aes_decrypt
from backend.service.v1_service import CeleryService,ReportGenerateService
import datetime

router = Blueprint('rule', __name__)


@router.post('/rule_group/create')
@record_user_operation(operation_manage='规则分组',operation_details='创建规则分组',operation_type='创建')
def rule_group_create():
    data = request.get_json()
    group_name = data.get('group_name')
    parent_id = data.get('parent_id', None)
    try:
        GenericCRUD.create(RuleGroup, group_name=group_name, parent_id=parent_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/rule_group/query')
def rule_group_query():
    try:
        result = RuleGroupGraph.get_query()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/rule_group/update')
@record_user_operation(operation_manage='规则分组',operation_details='修改规则分组',operation_type='修改')
def rule_group_update():
    data = request.get_json()
    id = data.get('id')
    group_name = data.get('group_name')
    parent_id = data.get('parent_id', None)
    try:
        if parent_id:
            GenericCRUD.update(RuleGroup, id=id, group_name=group_name, parent_id=parent_id)
        else:
            GenericCRUD.update(RuleGroup, id=id, group_name=group_name)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/rule_group/delete')
@record_user_operation(operation_manage='规则分组',operation_details='删除规则分组',operation_type='删除')
def rule_group_delete():
    data = request.get_json()
    id = data.get('id')
    try:
        GenericCRUD.delete(RuleGroup, id=id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/rule/create')
@record_user_operation(operation_manage='规则管理',operation_details='创建规则',operation_type='创建')
def rule_create():
    data = request.get_json()
    rule_code = data.get('rule_code')
    group_id = data.get('group_id')
    business_rules = data.get('business_rules')
    database_type = data.get('database_type')
    expression = data.get('expression')
    sql_expression = data.get('sql_expression')
    re_expression = data.get('re_expression')
    describe = data.get('describe')
    question_level = data.get('question_level')
    weight = data.get('weight')
    refer_text = data.get('refer_text')
    is_active = data.get('is_active')
    rule_type = data.get('rule_type')
    up_cycle = data.get('up_cycle')
    dimension = data.get('dimension')
    is_timeliness = data.get('is_timeliness')
    try:
        sql_expression =aes_decrypt(sql_expression)
        if is_sql_injection_risky(sql_expression) is True:
            return ErrorResponse(error_data='检测到sql注入风险').to_response()
        GenericCRUD.create(Rule,
                           rule_code=rule_code,
                           group_id=group_id,
                           business_rules=business_rules,
                           database_type=database_type,
                           expression=expression,
                           sql_expression=sql_expression,
                           re_expression=re_expression,
                           describe=describe,
                           question_level=question_level,
                           weight=weight,
                           is_active=is_active,
                           rule_type=rule_type,
                           up_cycle=up_cycle,
                           refer_text=refer_text,
                           dimension=dimension,
                           is_timeliness=is_timeliness
                           )
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/rule/update')
@record_user_operation(operation_manage='规则管理',operation_details='修改规则信息',operation_type='修改')
def rule_update():
    data = request.get_json()
    id = data.get('id')
    rule_code = data.get('rule_code')
    group_id = data.get('group_id')
    business_rules = data.get('business_rules')
    database_type = data.get('database_type')
    expression = data.get('expression')
    sql_expression = data.get('sql_expression')
    re_expression = data.get('re_expression')
    describe = data.get('describe')
    question_level = data.get('question_level')
    weight = data.get('weight')
    is_active = data.get('is_active')
    rule_type = data.get('rule_type')
    up_cycle = data.get('up_cycle')
    try:
        sql_expression =aes_decrypt(sql_expression)
        if is_sql_injection_risky(sql_expression) is True:
            return ErrorResponse(error_data='检测到sql注入风险').to_response()
        GenericCRUD.update(Rule,
                           id=id,
                           rule_code=rule_code,
                           group_id=group_id,
                           business_rules=business_rules,
                           database_type=database_type,
                           expression=expression,
                           sql_expression=sql_expression,
                           re_expression=re_expression,
                           describe=describe,
                           question_level=question_level,
                           weight=weight,
                           is_active=is_active,
                           rule_type=rule_type,
                           up_cycle=up_cycle
                           )
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/rule/query')
def rule_query():
    data = request.get_json()
    page = data.get('page', 1)
    rule_name = data.get('rule_name')
    per_page = data.get('per_page', 9999)
    group_id = data.get('group_id', None)
    dimension = data.get('dimension')
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        if group_id is None:
            rule_info = GenericCRUD.query_by_conditions(Rule)
            if dimension:
                rule_info = GenericCRUD.query_by_conditions(Rule,filters={'dimension':dimension})
        else:
            rule_info = RuleGraph.get_query_by_group_id(group_id=group_id,dimension=dimension)
        if rule_name:
            rule_info = [i for i in rule_info if i.get('rule_code').find(rule_name) != -1]
        data = Pagination(rule_info,page, per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/rule/query/filter')
def rule_query_filter():
    data = request.get_json()
    type = data.get('type', 'field')
    is_timeliness = data.get('is_timeliness', False)
    result = {
    }
    try:
        def get_rule_group_tree(parent_id=None):
            group_info = GenericCRUD.query_by_conditions(RuleGroup, filters={"parent_id": parent_id})
            result = []
            for i in group_info:
                sub_groups = get_rule_group_tree(i['id'])
                rule_info = GenericCRUD.query_by_conditions(Rule, filters={"group_id": i['id'], 'dimension': type,
                                                                           'is_timeliness': is_timeliness})
                for rule in rule_info:
                    rule['name'] = rule['rule_code']
                    rule['leaf'] = True
                group_info = {
                    'name': i['group_name'],
                    'id': i['id'],
                    'children': sub_groups,
                    'rule_info': rule_info,
                    'leaf': False
                }
                result.append(group_info)
            return result
        group_info = get_rule_group_tree()
        result['data'] = group_info
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/rule/delete')
@record_user_operation(operation_manage='规则管理', operation_details='删除规则',operation_type='删除')
def rule_delete():
    data = request.get_json()
    rule_id = data.get('rule_id', None)
    try:
        if rule_id is None:
            raise Exception('rule_id is None')
        else:
            GenericCRUD.delete(Rule, rule_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/datasource/query')
def datasource_query():
    data = request.get_json()
    datasource_name = data.get('datasource_name')
    system_name = data.get('system_name')
    dept_id = data.get('dept_id')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    page = data.get('page', 1)
    per_page = data.get('per_page', None)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        datasource_infos = GenericCRUD.query_by_conditions(DatasourceInfo, order_by=['-id'])
        if datasource_name:
            datasource_infos = GenericCRUD.query_by_conditions(DatasourceInfo,conditions=DatasourceInfo.datasource_name.like(f'%{datasource_name}%'), order_by=['-id'])
        for i in datasource_infos:
            system_info = GenericCRUD.query_by_conditions(BelongSystem, filters={"id": i['belonging_system_id']}, first=True)
            i['execute_time'] = GenericCRUD.query_by_conditions(QualityExecute, filters={"database_id": i['id']},
                                                                first=True).get('execute_time')
            i['system_name'] = system_info.get('system_name')
            i['department'] = system_info.get('department')
            i['belonging_department'] = system_info.get('belonging_department')
            i['dept_id'] = str(system_info.get('department_id'))
        if per_page == None:
            per_page = len(datasource_infos)
        if system_name:
            datasource_infos = [i for i in datasource_infos if i.get('system_name').find(system_name) != -1]
        elif dept_id:
            datasource_infos = [i for i in datasource_infos if i.get('dept_id') == dept_id]
        elif system_name and dept_id:
            datasource_infos = [i for i in datasource_infos if i.get('system_name').find(system_name) != -1 and i.get('dept_id') == dept_id]
        if sort_key:
            datasource_infos = sorted(
                [x for x in datasource_infos if x.get(sort_key) is not None],
                key=lambda x: x.get(sort_key),
                reverse=True if order == 'desc' else False
            ) + [x for x in datasource_infos if x.get(sort_key) is None]

        data = Pagination(items=datasource_infos, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/table/query')
def table_query():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    table_name = data.get('table_name')
    page = data.get('page', 1)
    per_page = data.get('per_page', None)
    sort_key = data.get('sort_key')
    order = data.get('order','desc')
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        table_history_info = GenericCRUD.query_by_conditions(model_class=TableInfo,
                                                             filters={"datasource_id": datasource_id})
        if table_name:
            table_history_info = GenericCRUD.query_by_conditions(model_class=TableInfo,
                                                                 filters={"datasource_id": datasource_id},
                                                                 conditions=TableInfo.table_name.like(f'%{table_name}%'))
        for i in table_history_info:
            rule_id = GenericCRUD.query_by_conditions(model_class=ConfigureRuleInfo,
                                                      filters={"table_id": i['id'], "field_id": None})
            quality_execute = GenericCRUD.query_by_conditions(QualityExecute,
                                                              filters={"database_id": datasource_id,
                                                                       'quality_table_id': i.get('id')},
                                                              first=True)
            configure_timeliness = GenericCRUD.query_by_conditions(ConfigureTimelinessInfo,filters={'table_id': i.get('id')},first=True)
            i['up_cycle'] = configure_timeliness.get('up_cycle')
            i['execute_time'] = quality_execute.get('execute_time')
            i['execute_status'] = quality_execute.get('execute_status')
            rule_object = [GenericCRUD.query_by_conditions(Rule, filters={"id": i.get('rule_id')}, first=True) for i in rule_id]
            i['rule_object'] = [{'id': i.get('id'),'name':i.get('rule_code')} for i in rule_object if i != {}]
        if per_page == None:
            per_page = len(table_history_info)
        if sort_key:
            table_history_info = sorted(table_history_info, key=lambda x: x.get(sort_key), reverse=True if order == 'desc' else False)
        data = Pagination(items=table_history_info, page=page,per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/field/query')
def field_query():
    data = request.get_json()
    table_id = data.get('table_id')
    field_name = data.get('field_name')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        field_history_info = GenericCRUD.query_by_conditions(model_class=FieldInfo,
                                                             filters={"table_info_id": table_id},
                                                             order_by=['-id'])
        if field_name:
            field_history_info = GenericCRUD.query_by_conditions(model_class=FieldInfo,
                                                                 filters={"table_info_id": table_id},
                                                                 conditions=FieldInfo.name.like(f'%{field_name}%'),
                                                                 order_by=['-id'])
        for i in field_history_info:
            quality_execute = GenericCRUD.query_by_conditions(QualityExecute,
                                                              filters={"database_id": i['id'],
                                                                       'quality_field_id': i.get('id')},
                                                              first=True)
            i['execute_time'] = quality_execute.get('execute_time')
            i['execute_status'] = quality_execute.get('execute_status')
            rule_id = GenericCRUD.query_by_conditions(model_class=ConfigureRuleInfo, filters={"field_id": i['id']})
            rule_info = [GenericCRUD.query_by_conditions(Rule, filters={"id": i.get('rule_id')}, first=True) for i in rule_id]
            i['rule_object'] = [{'id': i.get('id'),'name':i.get('rule_code')} for i in rule_info]
        data = Pagination(items=field_history_info,
                          page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/configure/rule')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='配置规则',operation_type='配置')
def configure_rule():
    data = request.get_json()
    rules_id = data.get('rules_id')
    field_id = data.get('field_id')
    table_id = data.get('table_id')
    datasource_id = data.get('datasource_id')
    is_timeliness = data.get('is_timeliness',False)
    try:
        config_rule_info = GenericCRUD.query_by_conditions(ConfigureRuleInfo,
                                                           filters={"field_id": field_id, "table_id": table_id,
                                                                    'datasource_id': datasource_id})

        for i in config_rule_info:
            rule_info = GenericCRUD.query_by_conditions(Rule, filters={"id": i.get('rule_id')}, first=True)
            if rule_info.get('is_timeliness') == is_timeliness:
                GenericCRUD.delete(ConfigureRuleInfo, i.get('id'))
        for rule_id in rules_id:
            GenericCRUD.create(ConfigureRuleInfo, rule_id=rule_id, field_id=field_id, table_id=table_id,
                               datasource_id=datasource_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/configure/rule/batch')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='批量配置规则',operation_type='配置')
def configure_rule_batch():
    data = request.get_json()
    rules_id = data.get('rules_id',[])
    table_id = data.get('table_id',[])
    field_id = data.get('field_id')
    datasource_id = data.get('datasource_id')
    is_timeliness = data.get('is_timeliness', False)
    try:
        for _table_id in table_id:
            if not field_id:
                config_rule_info = GenericCRUD.query_by_conditions(ConfigureRuleInfo,
                                                               filters={"table_id": _table_id,
                                                                        'datasource_id': datasource_id})
            else:
                config_rule_info = GenericCRUD.query_by_conditions(ConfigureRuleInfo,
                                                               filters={"table_id": _table_id,
                                                                        'datasource_id': datasource_id},
                                                               conditions=ConfigureRuleInfo.field_id.in_(field_id))
            for i in config_rule_info:
                rule_info = GenericCRUD.query_by_conditions(Rule, filters={"id": i.get('rule_id')}, first=True)
                if rule_info.get('is_timeliness') == is_timeliness:
                    GenericCRUD.delete(ConfigureRuleInfo, i.get('id'))
                GenericCRUD.delete(ConfigureRuleInfo, i.get('id'))
            for rule_id in rules_id:
                if field_id:
                    for _field_id in field_id:
                        GenericCRUD.create(ConfigureRuleInfo, rule_id=rule_id, table_id=_table_id,field_id=_field_id,
                                           datasource_id=datasource_id)
                else:
                    GenericCRUD.create(ConfigureRuleInfo, rule_id=rule_id, table_id=_table_id,
                                       datasource_id=datasource_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/configure/rule/field/')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='配置多字段规则',operation_type='配置')
def configure_rule_field():
    data = request.get_json()
    rules_id = data.get('rule_id')
    field_id1 = data.get('field_id1')
    field_id2 = data.get('field_id2')
    table_id = data.get('table_id')
    datasource_id = data.get('datasource_id')
    try:
        GenericCRUD.create(ConfigureRuleFieldInfo, rule_id=rules_id, field_id1=field_id1, field_id2=field_id2, table_id=table_id,datasource_id=datasource_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/configure/rule/field/delete')
@record_user_operation(operation_type='operation_manage',operation_details='删除多字段规则',operation_manage='删除')
def configure_rule_field_delete():
    data = request.get_json()
    id = data.get('id')
    try:
        GenericCRUD.delete(ConfigureRuleFieldInfo, id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/configure/rule/table/')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='配置多表规则',operation_type='配置')
def configure_rule_table():
    data = request.get_json()
    rules_id = data.get('rule_id')
    table_id1 = data.get('table_id1')
    table_id2 = data.get('table_id2')
    field_id1 = data.get('field_id1')
    field_id2 = data.get('field_id2')
    datasource_id = data.get('datasource_id')
    try:
        GenericCRUD.create(ConfigureRuleTableInfo, rule_id=rules_id, table_id1=table_id1, table_id2=table_id2, field_id1=field_id1, field_id2=field_id2, datasource_id=datasource_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/configure/rule/table/delete')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='删除多表规则',operation_type='删除')
def configure_rule_table_delete():
    data = request.get_json()
    id = data.get('id')
    try:
        GenericCRUD.delete(ConfigureRuleTableInfo, id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/rule/query/field')
def rule_query_field():
    data = request.get_json()
    table_id = data.get('table_id')
    datasource_id = data.get('datasource_id')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        configure_rule_field_info = GenericCRUD.query_by_conditions(ConfigureRuleFieldInfo, filters={'table_id': table_id, 'datasource_id': datasource_id})
        for i in configure_rule_field_info:
            rule_info = GenericCRUD.query_by_conditions(Rule, filters={"id": i.get('rule_id')}, first=True)
            field1_info = GenericCRUD.query_by_conditions(FieldHistoryInfo, filters={'id':i.get('field_id1')}, first=True)
            field2_info = GenericCRUD.query_by_conditions(FieldHistoryInfo, filters={'id':i.get('field_id2')}, first=True)
            i['field1_name'] = field1_info.get('name')
            i['field2_name'] = field2_info.get('name')
            i['rule_name'] = rule_info.get('rule_code')
        result_data = Pagination(configure_rule_field_info, page, per_page)
        result['data'] = result_data.get_items()
        result['count'] = result_data.total
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/rule/query/table')
def rule_query_table():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        configure_rule_table_info = GenericCRUD.query_by_conditions(ConfigureRuleTableInfo, filters={'datasource_id': datasource_id})
        for i in configure_rule_table_info:
            rule_info = GenericCRUD.query_by_conditions(Rule, filters={"id": i.get('rule_id')}, first=True)
            table1_info = GenericCRUD.query_by_conditions(TableHistoryTemplateInfo, filters={'id':i.get('table_id1')}, first=True)
            table2_info = GenericCRUD.query_by_conditions(TableHistoryTemplateInfo, filters={'id':i.get('table_id2')}, first=True)
            field1_info = GenericCRUD.query_by_conditions(FieldHistoryInfo, filters={'id':i.get('field_id1')}, first=True)
            field2_info = GenericCRUD.query_by_conditions(FieldHistoryInfo, filters={'id':i.get('field_id2')}, first=True)
            i['field1_name'] = field1_info.get('name')
            i['field2_name'] = field2_info.get('name')
            i['table1_name'] = table1_info.get('table_name')
            i['table2_name'] = table2_info.get('table_name')
            i['rule_name'] = rule_info.get('rule_code')
        result_data = Pagination(configure_rule_table_info, page, per_page)
        result['data'] = result_data.get_items()
        result['count'] = result_data.total
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/schedule/create')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='创建规则定时任务',operation_type='创建')
def schedule_create():
    data = request.get_json()
    minute = data.get('minute')
    hour = data.get('hour')
    day = data.get('day')
    week = data.get('week')
    method = data.get('method')
    schedule_name = data.get('schedule_name')
    datasource_id = data.get('datasource_id')
    table_id = data.get('table_id', None)
    try:
        GenericCRUD.create(QualitySchedulerInfo, minute=minute, hour=hour, day=day, week=week,
                           schedule_name=schedule_name, datasource_id=datasource_id, table_id=table_id, method=method)
        data['schedule_type'] = 'data_quality'
        r.publish('scheduler',json.dumps(data))
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/rule/schedule/stop')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='停止正在运行的规则任务',operation_type='停止')
def rule_schedule_stop():
    data = request.get_json()
    execute_id = data.get('execute_id')
    try:
        GenericCRUD.update(QualityExecute, execute_id, execute_status='暂停')
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/schedule/query')
def schedule_query():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_name = data.get('datasource_name')
    dept_id = data.get('dept_id')
    system_name = data.get('system_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo)
        for datasource in datasource_info:
            system_info = GenericCRUD.query_by_conditions(BelongSystem, filters={'id': datasource.get('belonging_system_id')}, first=True)
            schedule_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'datasource_id': datasource.get('id')},first=True)
            execute_info = GenericCRUD.query_by_conditions(QualityExecute, filters={'database_id': datasource.get('id')},order_by='-created_at',first=True)
            datasource['system_name'] = system_info.get('system_name')
            datasource['department'] = system_info.get('department')
            datasource['belonging_department'] = system_info.get('belonging_department')
            datasource['schedule_name'] = schedule_info.get('schedule_name')
            datasource['table_id'] = schedule_info.get('table_id')
            datasource['schedule_status'] = schedule_info.get('is_start')
            datasource['execute_time'] = execute_info.get('execute_time')
            datasource['method'] = schedule_info.get('method')
            datasource['hour'] = schedule_info.get('hour')
            datasource['minute'] = schedule_info.get('minute')
            datasource['day'] = schedule_info.get('day')
            datasource['week'] = schedule_info.get('week')
        if datasource_name and dept_id and system_name:
            datasource_info = [i for i in datasource_info if i.get('datasource_name').find(datasource_name) != -1 and i.get('dept_id') == dept_id and i.get('system_name').find(system_name) != -1]
        elif datasource_name and dept_id:
            datasource_info = [i for i in datasource_info if i.get('datasource_name').find(datasource_name) != -1 and i.get('dept_id')== dept_id]
        elif datasource_name and system_name:
            datasource_info = [i for i in datasource_info if i.get('datasource_name').find(datasource_name) != -1 and i.get('system_name').find(system_name) != -1]
        elif dept_id and system_name:
            datasource_info = [i for i in datasource_info if i.get('dept_id') == dept_id and i.get('system_name').find(system_name) != -1]
        elif datasource_name:
            datasource_info = [i for i in datasource_info if i.get('datasource_name').find(datasource_name) != -1]
        elif dept_id:
            datasource_info = [i for i in datasource_info if i.get('dept_id') == dept_id]
        elif system_name:
            datasource_info = [i for i in datasource_info if i.get('system_name').find(system_name) != -1]
        if sort_key:
            datasource_info = sorted(
                datasource_info,
                key=lambda x: (x.get(sort_key) is None, x.get(sort_key)),
                reverse=True if order == 'desc' else False
            )

        data = Pagination(items=datasource_info, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/schedule/detail')
def query_schedule_detail():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id', None)
    execute_status = data.get('execute_status', None)
    schedule_name = data.get('schedule_name', None)
    system_name = data.get('system_name', None)
    start_time = data.get('start_time', None)
    end_time = data.get('end_time', None)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        quality_execute_info = GenericCRUD.query_by_conditions(QualityExecute, filters={'rule_type':'规则检查'},order_by='-created_at')
        if datasource_id:
            quality_execute_info = GenericCRUD.query_by_conditions(QualityExecute, filters={'database_id': datasource_id,'rule_type':'规则检查'},order_by='-created_at')
        for quality_execute in quality_execute_info:
            datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo,filters={'id':quality_execute.get('database_id')},first=True)
            system_info = GenericCRUD.query_by_conditions(BelongSystem,filters={'id':datasource_info.get('belonging_system_id')},first=True)
            quality_execute['datasource_name'] = datasource_info.get('datasource_name')
            quality_execute['datasource_type'] = datasource_info.get('database_type')
            quality_execute['system_name'] = system_info.get('system_name')
            quality_execute['department'] = system_info.get('department')
            quality_execute['belonging_department'] = system_info.get('belonging_department')
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') if start_time else None
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') if end_time else None
        if start_time and end_time:
            quality_execute_info = [i for i in quality_execute_info if i.get('created_at') >= start_time and i.get('created_at') <= end_time]
        if execute_status:
            quality_execute_info = [i for i in quality_execute_info if i.get('execute_status') == execute_status]
        if schedule_name:
            quality_execute_info = [i for i in quality_execute_info if i.get('schedule_name').find(schedule_name) != -1]
        elif system_name:
            quality_execute_info = [i for i in quality_execute_info if i.get('system_name').find(system_name) != -1]
        data = Pagination(items=quality_execute_info, page=page, per_page=per_page)
        result['data'] = data.get_items()
        result['count'] = data.total
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/schedule/detail/table')
def schedule_detail_table():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id')
    execute_id = data.get('execute_id')
    _table_name = data.get('table_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    vague_keys_to_filter = [
    'table_no_comment', 'is_have_primary_keys','timeliness'
    ]
    vague_filter_dict = {key: data[key] for key in vague_keys_to_filter if data.get(key) is not None}
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        result_data = []
        quality_rating_details = GenericCRUD.query_by_conditions(QualityReportResult, filters={'execute_id':execute_id,'database_id':datasource_id},order_by='-created_at')
        for quallity_rating in quality_rating_details:
            if quallity_rating.get('table_id'):
                table_name = GenericCRUD.query_by_conditions(TableInfo, filters={'id': quallity_rating.get('table_id')},
                                                             first=True).get('table_name')
                configure_rule = GenericCRUD.query_by_conditions(ConfigureRuleInfo, filters={'table_id': quallity_rating.get('table_id')},
                                                                 first=True)
                rule_type = GenericCRUD.query_by_conditions(Rule, filters={'id': configure_rule.get('rule_id')},
                                                            first=True).get('rule_code')
                normative_info = GenericCRUD.query_by_conditions(QualityNormative, filters={'execute_id': execute_id,
                                                                                            'quality_table_id': quallity_rating.get('table_id')},
                                                                 first=True)
                timeliness_info = GenericCRUD.query_by_conditions(QualityTimeliness, filters={'execute_id': execute_id,
                                                                                              'database_id': datasource_id,
                                                                                              'quality_table_name': table_name},
                                                                  first=True)
                quallity_rating['table_id'] = quallity_rating.get('table_id')
                quallity_rating['table_name'] = table_name
                quallity_rating['rule_type'] = rule_type
                quallity_rating['execute_status'] = '已完成'
                quallity_rating['start_time'] = quallity_rating.get('created_at')
                quallity_rating['end_time'] = quallity_rating.get('created_at')
                quallity_rating['table_no_comment'] = normative_info.get('table_no_comment')
                quallity_rating['field_count'] = normative_info.get('field_count')
                quallity_rating['field_no_comment'] = normative_info.get('field_no_comment')
                quallity_rating['is_have_primary_keys'] = normative_info.get('is_have_primary_keys')
                quallity_rating['timeliness'] = timeliness_info.get('timeliness')
                quallity_rating['execute_log'] = "success"
                quallity_rating['log_text'] = '无'
                result_data.append(quallity_rating)
        for item in vague_filter_dict.keys():
            result_data = [i for i in result_data if str(i.get(item)) == str(vague_filter_dict[item])]
        if _table_name:
            result_data = [i for i in result_data if i.get('table_name').find(_table_name) != -1]
        if sort_key:
            result_data = sorted(
                result_data,
                key=lambda x: (x.get(sort_key) is None, x.get(sort_key)),
                reverse=True if order == 'desc' else False
            )
        result_data = Pagination(items=result_data, page=page, per_page=per_page)
        result['data'] = result_data.get_items()
        result['count'] = result_data.total
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/schedule/detail/table/update')
def schedule_detail_table_update():
    data = request.get_json()
    execute_id = data.get('execute_id')
    datasource_id = data.get('database_id')
    table_name = data.get('table_name')
    id = data.get('id')
    total = data.get('total')
    timeliness = data.get('timeliness')
    try:
        timeliness_info = GenericCRUD.query_by_conditions(QualityTimeliness, filters={'execute_id': execute_id,
                                                                                      'database_id': datasource_id,
                                                                                      'quality_table_name': table_name},
                                                          first=True)
        print(timeliness_info.get('id'))
        GenericCRUD.update(QualityTimeliness, id=timeliness_info.get('id'), timeliness=timeliness)
        GenericCRUD.update(QualityReportResult, id=id, total=total)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/schedule/detail/field')
def schedule_detail_field():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id')
    execute_id = data.get('execute_id')
    table_id = data.get('table_id')
    field_name = data.get('field_name')
    execute_status = data.get('execute_status')
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        integrity_info = GenericCRUD.query_by_conditions(QualityIntegrity, filters={'execute_id':execute_id,'database_id':datasource_id,'table_id':table_id},order_by='-created_at')
        for quality_integrity in integrity_info:
            rule_info = GenericCRUD.query_by_conditions(Rule, filters={'id': quality_integrity.get('rule_id')},
                                                        first=True)
            field_info = GenericCRUD.query_by_conditions(FieldInfo, filters={'table_info_id': quality_integrity.get('table_id'),'name':quality_integrity.get('quality_field_name')},first=True)
            quality_integrity['field_type'] = field_info.get('type')
            quality_integrity['rule_type'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                quality_integrity['quality_field_name'] = None
            if quality_integrity['execute_log'] is None:
                quality_integrity['execute_status'] = '成功'
                quality_integrity['log_text'] = '无'
            else:
                quality_integrity['execute_status'] = '失败'
                quality_integrity['log_text'] = '错误信息'

        repeatability_info = GenericCRUD.query_by_conditions(QualityRepeatability,filters={'execute_id':execute_id,'database_id':datasource_id,'table_id':table_id},order_by='-created_at')

        for quality_repeatability in repeatability_info:
            rule_info = GenericCRUD.query_by_conditions(Rule,filters={'id':quality_repeatability.get('rule_id')},first=True)
            field_info = GenericCRUD.query_by_conditions(FieldInfo, filters={'table_info_id': quality_repeatability.get('table_id'),'name':quality_repeatability.get('quality_field_name')},first=True)
            quality_repeatability['field_type'] = field_info.get('type')
            quality_repeatability['rule_type'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                quality_repeatability['quality_field_name'] = None
            if quality_repeatability['execute_log']  is None:
                quality_repeatability['execute_status'] = '成功'
                quality_repeatability['log_text'] = '无'
            else:
                quality_repeatability['execute_status'] = '失败'
                quality_repeatability['log_text'] = '错误信息'
        accuracy_info = GenericCRUD.query_by_conditions(QualityAccuracy,filters={'execute_id':execute_id,'database_id':datasource_id,'table_id':table_id},order_by='-created_at')
        for quality_accuracy in accuracy_info:
            rule_info = GenericCRUD.query_by_conditions(Rule,filters={'id':quality_accuracy.get('rule_id')},first=True)
            field_info = GenericCRUD.query_by_conditions(FieldInfo, filters={'table_info_id': quality_accuracy.get('table_id'),'name':quality_accuracy.get('quality_field_name')},first=True)
            quality_accuracy['field_type'] = field_info.get('type')
            quality_accuracy['rule_type'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                quality_accuracy['quality_field_name'] = None
            if quality_accuracy['execute_log']  is None:
                quality_accuracy['execute_status'] = '成功'
                quality_accuracy['log_text'] = '无'
            else:
                quality_accuracy['execute_status'] = '失败'
                quality_accuracy['log_text'] = '错误信息'
        consistency_info = GenericCRUD.query_by_conditions(QualityConsistency,filters={'execute_id':execute_id,'database_id':datasource_id,'table_id':table_id},order_by='-created_at')
        for quality_consistency in consistency_info:
            rule_info = GenericCRUD.query_by_conditions(Rule,filters={'id':quality_consistency.get('rule_id')},first=True)
            field_info = GenericCRUD.query_by_conditions(FieldInfo, filters={'table_info_id': quality_consistency.get('table_id'),'name':quality_consistency.get('quality_field_name')},first=True)
            quality_consistency['field_type'] = field_info.get('type')
            quality_consistency['rule_type'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                quality_consistency['quality_field_name'] = None
            if quality_consistency['execute_log']  is None:
                quality_consistency['execute_status'] = '成功'
                quality_consistency['log_text'] = '无'
            else:
                quality_consistency['execute_status'] = '失败'
                quality_consistency['log_text'] = '错误信息'
        result_info = integrity_info + repeatability_info + accuracy_info + consistency_info
        if field_name:
            result_info = [info for info in result_info if info.get('quality_field_name').find(field_name) != -1]
        elif execute_status:
            result_info = [info for info in result_info if info.get('execute_status') == execute_status]
        data = Pagination(items=result_info, page=page, per_page=per_page)
        result['data'] = data.get_items()
        result['count'] = data.total
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/schedule/update')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='修改规则定时任务',operation_type='修改')
def schedule_update():
    data = request.get_json()
    minute = data.get('minute')
    hour = data.get('hour')
    day = data.get('day')
    week = data.get('week')
    method = data.get('method')
    schedule_name = data.get('schedule_name')
    datasource_id = data.get('datasource_id')
    table_id = data.get('table_id', None)
    try:
        quality_scheduler_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'id': datasource_id}, first=True)
        if quality_scheduler_info == {}:
            GenericCRUD.create(QualitySchedulerInfo,id=datasource_id, minute=minute, hour=hour, day=day, week=week,
                           schedule_name=schedule_name, datasource_id=datasource_id, table_id=table_id, method=method)
        else:
            GenericCRUD.update(QualitySchedulerInfo, datasource_id, minute=minute, hour=hour, day=day, week=week,
                           schedule_name=schedule_name, datasource_id=datasource_id, table_id=table_id, method=method, is_start=True)
        data['schedule_type'] = 'data_quality'
        r.publish('scheduler',json.dumps(data))
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/schedule/stop')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='停止规则定时任务',operation_type='停止')
def schedule_stop():
    data = request.get_json()
    schedule_id = data.get('datasource_id')
    try:
        schedule_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'id': schedule_id}, first=True)
        if schedule_info.get('is_start') is False:
            return ErrorResponse(error_data='请先启动定时任务').to_response()
        data['schedule_type'] = 'delete'
        data['id'] = 'quality_' + str(schedule_id)
        r.publish('delete', json.dumps(data))
        GenericCRUD.update(QualitySchedulerInfo, schedule_id, is_start=False)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/schedule/start')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='启动规则定时任务',operation_type='启动')
def schedule_start():
    data = request.get_json()
    schedule_id = data.get('datasource_id')
    try:
        schedule_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'id': schedule_id}, first=True)
        if schedule_info.get('is_start') is True:
            return ErrorResponse(error_data='定时任务已启动').to_response()
        data['schedule_type'] = 'data_quality'
        data['minute'] = schedule_info.get('minute')
        data['hour'] = schedule_info.get('hour')
        data['day'] = schedule_info.get('day')
        data['week'] = schedule_info.get('week')
        data['method'] = schedule_info.get('method')
        r.publish('scheduler', json.dumps(data))
        GenericCRUD.update(QualitySchedulerInfo, schedule_id, is_start=True)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/schedule/delete')
@record_user_operation(operation_manage='数据质量规则配置',operation_details='删除规则定时任务',operation_type='删除')
def schedule_delete():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    try:
        schedule_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'id': schedule_id}, first=True)
        if schedule_info.get('is_start') is True:
            return ErrorResponse(error_data='请先停止定时任务').to_response()
        GenericCRUD.delete(QualitySchedulerInfo, schedule_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()


@router.post('/schedule/details/query')
def schedule_details_query():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        data = []
        schedule_group_info = GenericCRUD.query_by_conditions_group(QualityExecute,group_by=['schedule_id','quality_table_id'],filters={'schedule_id': schedule_id})
        for _,table_id in schedule_group_info:
            _data = {}
            schedule_info = GenericCRUD.query_by_conditions(QualityExecute, filters={'schedule_id': schedule_id,'quality_table_id':table_id},order_by='-created_at',first=True)
            _schedule_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'id': schedule_id}, first=True)
            schedule_name = _schedule_info.get('schedule_name')
            datasource_name = GenericCRUD.query_by_conditions(DatasourceInfo, filters={'id': schedule_info.get('database_id')}, first=True).get('datasource_name')
            table_name = GenericCRUD.query_by_conditions(TableInfo, filters={'id': table_id}, first=True).get('table_name')
            _data['schedule_name'] = schedule_name
            _data['datasource_name'] = datasource_name
            _data['table_name'] = table_name
            _data['table_id'] = table_id
            _data['execute_time'] = schedule_info.get('execute_time')
            _data['updated_at'] = schedule_info.get('updated_at')
            data.append(_data)
        data = Pagination(items=data, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count

    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/schedule/details/field/query')
def schedule_details_field_query():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    table_id = data.get('table_id')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        schedule_execute = GenericCRUD.query_by_conditions(QualityExecute, filters={'schedule_id': schedule_id,'quality_table_id':table_id},order_by='-created_at')
        for _schedule_execute in schedule_execute:
            field_info = GenericCRUD.query_by_conditions(FieldHistoryInfo, filters={'id': _schedule_execute.get('quality_field_id')},first=True)
            _schedule_info = GenericCRUD.query_by_conditions(QualitySchedulerInfo, filters={'id': schedule_id}, first=True)
            schedule_name = _schedule_info.get('schedule_name')
            _schedule_execute['schedule_name'] = schedule_name
            _schedule_execute['field_name'] = field_info.get('name')
        data = Pagination(items=schedule_execute, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/rule/run')
# @record_user_operation(operation_manage='数据质量规则配置',operation_details='执行规则检测',operation_type='启动')
def rule_run():
    data = request.get_json()
    datasource_ids = data.get('datasource_id',[])
    table_ids = data.get('table_id',[])
    try:
        for datasource_id in datasource_ids:
            if len(table_ids) == 0:
                CeleryService.send_create_task(database_id=datasource_id, table_id=None)
            else:
                for table_id in table_ids:
                    CeleryService.send_create_task(database_id=datasource_id, table_id=table_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/rule/timeliness/run')
@record_user_operation(operation_manage='数据及时性检测',operation_details='执行时效性规则检测',operation_type='启动')
def rule_timeliness_run():
    data = request.get_json()
    datasource_ids = data.get('datasource_id',[])
    table_ids = data.get('table_id',[])
    try:
        for datasource_id in datasource_ids:
            if len(table_ids) == 0:
                CeleryService.send_timeliness_detection_task(database_id=datasource_id, table_id=None)
            else:
                for table_id in table_ids:
                    CeleryService.send_timeliness_detection_task(database_id=datasource_id, table_id=table_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/generate/report')
# @record_user_operation(operation_type='生成报告')
def generate_report():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    execute_id = data.get('execute_id')
    table_id = data.get('table_id')
    try:
        if table_id:
            table_ids = GenericCRUD.query_by_conditions(QualityReportResult, filters={'database_id': datasource_id,'execute_id':execute_id,'table_id':table_id})
        else:
            table_ids = GenericCRUD.query_by_conditions(QualityReportResult, filters={'database_id': datasource_id,'execute_id':execute_id},conditions=QualityReportResult.table_id is not None)
        report_service = ReportGenerateService()
        all_rule_info = GenericCRUD.query_by_conditions(Rule)
        for table_id in table_ids:
            table_info = GenericCRUD.query_by_conditions(TableInfo, filters={'id': table_id.get('table_id')}, first=True)
            rule_info = GenericCRUD.query_by_conditions(ConfigureRuleInfo, filters={'table_id': table_id.get('table_id')})
            field_check_list = set()
            for rule in rule_info:
                if rule.get('field_id'):
                    field_info = GenericCRUD.query_by_conditions(FieldHistoryInfo, filters={'id': rule.get('field_id')}, first=True)
                    if field_info == {}:
                        continue
                    if field_info.get('comment'):
                        field_check_list.add(field_info.get('comment'))
                    else:
                        field_check_list.add(field_info.get('name'))
            file_name = str(execute_id) + str(table_id.get('table_id')) + '.pdf'
            data_directory_name = table_info.get('table_name') if table_info.get('table_comment') is None else table_info.get('table_comment')
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            random_number = ''.join(str(random.randint(0, 9)))
            report_code = timestamp + random_number
            check_date = datetime.datetime.now().strftime('%Y-%m-%d')
            check_total = table_id.get('total')
            data_total = table_info.get('data_total')
            field_count = table_info.get('field_count')
            rule_total = len(rule_info)
            field_info = ','.join(field_check_list)
            text = ""

            field_table_data = []
            quality_integrity = GenericCRUD.query_by_conditions(QualityIntegrity, filters={'execute_id': execute_id, 'table_id': table_id.get('table_id'),'execute_log':None})
            quality_repeatability = GenericCRUD.query_by_conditions(QualityRepeatability, filters={'execute_id': execute_id, 'table_id': table_id.get('table_id'),'execute_log':None})
            quality_accuracy = GenericCRUD.query_by_conditions(QualityAccuracy, filters={'execute_id': execute_id, 'table_id': table_id.get('table_id'),'execute_log':None})
            quality_consistency = GenericCRUD.query_by_conditions(QualityConsistency, filters={'execute_id': execute_id, 'table_id': table_id.get('table_id'),'execute_log':None})
            result_list = quality_integrity+quality_repeatability+quality_accuracy+quality_consistency
            for result in result_list:
                rule_info = GenericCRUD.query_by_conditions(Rule, filters={'id': result.get('rule_id')}, first=True)

                rule_name = rule_info.get('rule_code')
                field_name = result.get('quality_field_name')
                if rule_info.get('dimension') == 'table':
                    field_name = ''
                rule_refer_text = rule_info.get('refer_text')
                describe = '' if rule_info.get('describe') is None else rule_info.get('describe')
                dimension = '表级' if rule_info.get('dimension') == 'table' else '字段级'
                score = result.get('score')
                text += f"""
                        数据资源名称:{data_directory_name}
                        规则描述:{rule_refer_text}
                        字段信息:{field_name}
                        ------------------------------------------------
                """
                field_table_data.append([rule_name, field_name,describe, rule_refer_text,dimension,str(result.get('problem_lines')), str(score)])
            field_check_info = report_service.curl_llm_result(text)
            integrity = table_id.get('integrity') if table_id.get('integrity') else 0
            repeatability = table_id.get('repeatability') if table_id.get('repeatability') else 0
            accuracy = table_id.get('accuracy') if table_id.get('accuracy') else 0
            consistency = table_id.get('consistency') if table_id.get('consistency') else 0
            field_table_data2 = [integrity / 25 * 100, repeatability / 25 * 100, accuracy / 25 * 100, consistency / 25 * 100]
            field_table_data3 = []
            for rule in all_rule_info:
                field_table_data3.append([rule.get('rule_type'), rule.get('rule_code'),rule.get('describe'), rule.get('refer_text')])
            report_service.create_pdf(
                file_name=file_name,
                data_directory_name=data_directory_name,
                report_code=report_code,
                check_date=check_date,
                check_status='已完成',
                check_total=check_total,
                data_total=data_total,
                field_count=field_count,
                rule_total=rule_total,
                field_info=field_info,
                field_table_data=field_table_data,
                field_table_data2=field_table_data2,
                field_table_data3=field_table_data3
            )
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/stream')
def stream():
    # 假设我们有一个生成器函数 get_data_generator()
    data_gen = get_data_generator()
    gen_response = StreamResponse(data=data_gen)
    return gen_response.to_response()

def get_data_generator():
    # 这是一个示例生成器，实际应用中你应该从数据库或其他数据源获取数据
    for i in range(5):
        time.sleep(0.5)
        yield {"id": i, "value": f"Item {i}"}

@router.post('/report/query')
def report_query():
    data = request.get_json()
    datasource_name = data.get('datasource_name',None)
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        data = []
        quality_resport_result = GenericCRUD.query_by_conditions_group(QualityReportResult, group_by=['schedule_id','database_id'])
        for schedule_id, database_id in quality_resport_result:
            _data = {}
            _data['datasource_name'] = GenericCRUD.query_by_conditions(model_class=DatasourceInfo,
                                                                       filters={"id": database_id}, first=True).get(
                'datasource_name')
            all_quality_result = GenericCRUD.query_by_conditions(QualityReportResult,
                                                                 filters={"schedule_id": schedule_id})
            _data['schedule_name'] = GenericCRUD.query_by_conditions(QualitySchedulerInfo,
                                                                     filters={"id": schedule_id}, first=True).get('schedule_name')
            repeatability = sum(
                [i.get('repeatability') if i.get('repeatability') is not None else 0 for i in all_quality_result])
            integrity = sum([i.get('integrity') if i.get('integrity') is not None else 0 for i in all_quality_result])
            timeliness = sum(
                [i.get('timeliness') if i.get('timeliness') is not None else 0 for i in all_quality_result])
            _repeatability = round(repeatability / len(all_quality_result) if repeatability != 0 else 0, 2)
            _integrity = round(integrity / len(all_quality_result) if integrity != 0 else 0, 2)
            _data['schedule_id'] = schedule_id
            _data['repeatability'] = _repeatability
            _data['integrity'] = _integrity
            _data['timeliness'] = timeliness / len(all_quality_result) if timeliness != 0 else 0
            _data['database_id'] = database_id
            _data['created_at'] = all_quality_result[-1].get('created_at')
            _data['total'] = round(_repeatability + _integrity, 2)
            data.append(_data)
        if datasource_name:
            data = [i for i in data if i.get('datasource_name').find(datasource_name) != -1]
        data = Pagination(items=data, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/report/table/query')
def report_table_query():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    table_name = data.get('table_name',None)
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    result = {
        'page': page,
        'per_page': per_page
    }
    if order == 'desc':
        _order = '-{field}'
    else:
        _order = '{field}'
    try:
        table_info = GenericCRUD.query_by_conditions(QualityReportResult, filters={"schedule_id": schedule_id},order_by='-created_at')
        if table_name:
            table_info = GenericCRUD.query_by_conditions(QualityReportResult, filters={"schedule_id": schedule_id},order_by='-created_at',conditions=QualityReportResult.quality_table_name.like(f'%{table_name}%'))
        if sort_key:
            table_info = GenericCRUD.query_by_conditions(QualityReportResult, filters={"schedule_id": schedule_id},order_by=_order.format(field=sort_key))
        if sort_key and table_name:
            table_info = GenericCRUD.query_by_conditions(QualityReportResult, filters={"schedule_id": schedule_id},order_by=_order.format(field=sort_key),conditions=QualityReportResult.quality_table_name.like(f'%{table_name}%'))
        data = Pagination(items=table_info, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/report/field/query')
def report_field_query():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    table_name = data.get('table_name')
    field_name = data.get('field_name')
    query_type = data.get('type')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        if query_type == 'integrity':
            quality_result = GenericCRUD.query_by_conditions(QualityIntegrity,
                                                             filters={"database_id": datasource_id,
                                                                      "quality_table_name": table_name},order_by='-created_at')
            if field_name:
                quality_result = GenericCRUD.query_by_conditions(QualityIntegrity,
                                                                 filters={"database_id": datasource_id,
                                                                      "quality_table_name": table_name},
                                                                 conditions=QualityIntegrity.quality_field_name.like(f'%{field_name}%'),order_by='-created_at')
        elif query_type == 'repeatability':
            quality_result = GenericCRUD.query_by_conditions(QualityRepeatability,
                                                             filters={"database_id": datasource_id,
                                                                      "quality_table_name": table_name},order_by='-created_at')
            if field_name:
                quality_result = GenericCRUD.query_by_conditions(QualityRepeatability,
                                                                 filters={"database_id": datasource_id,
                                                                      "quality_table_name": table_name},
                                                                 conditions=QualityIntegrity.quality_field_name.like(f'%{field_name}%'),order_by='-created_at')
        elif query_type == 'timeliness':
            quality_result = GenericCRUD.query_by_conditions(QualityTimeliness,
                                                             filters={"database_id": datasource_id,
                                                                      "quality_table_name": table_name},order_by='-created_at')
            if field_name:
                quality_result = GenericCRUD.query_by_conditions(QualityTimeliness,
                                                                 filters={"database_id": datasource_id,
                                                                      "quality_table_name": table_name},
                                                                 conditions=QualityIntegrity.quality_field_name.like(f'%{field_name}%'),order_by='-created_at')
        else:
            return ErrorResponse(error_data='type参数错误').to_response()

        data = Pagination(items=quality_result, page=page, per_page=per_page)
        result_data = data.get_items()
        count = data.total
        result['data'] = result_data
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/report/field/total/query')
def report_field_total_query():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    table_name = data.get('table_name')
    field_names = data.get('field_name')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page,
        'data': []
    }
    try:
        for field_name in field_names:
            integrity = GenericCRUD.query_by_conditions(QualityIntegrity,
                                                        filters={"database_id": datasource_id,
                                                                 "quality_table_name": table_name,
                                                                 "quality_field_name": field_name},order_by='-created_at', first=True).get(
                'integrity')
            repeatability = GenericCRUD.query_by_conditions(QualityRepeatability,
                                                            filters={"database_id": datasource_id,
                                                                     "quality_table_name": table_name,
                                                                     "quality_field_name": field_name},order_by='-created_at', first=True).get(
                'repeatability')
            integrity = int(integrity) if integrity is not None else 0
            repeatability = int(repeatability) if repeatability is not None else 0
            total = integrity + repeatability
            result['data'].append({'field_name': field_name, 'total': total})
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/report/download')
@record_user_operation(operation_manage='数据质量评分',operation_details='下载报告',operation_type='下载')
def report_download():
    data = request.get_json()
    execute_id = data.get('execute_id')
    datasource_id = data.get('datasource_id')
    try:
        file_name = str(execute_id) + str(datasource_id) + '.pdf'
        file_path = config.get('report_file') + file_name
        print(file_path)
        if not os.path.exists(file_path):
            return ErrorResponse(error_data='文件不存在').to_response()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return FileResponse(file_path, filename=file_name).to_response()


@router.post('/create/normative')
@record_user_operation(operation_manage='库表规范检测',operation_details='创建规范性检查任务',operation_type='创建')
def create_normative():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    try:
        CeleryService.send_create_normative_task(datasource_id)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data='创建规范任务已提交').to_response()


@router.post('/query/timeliness/scheduler')
def query_timeliness_scheduler():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id',None)
    execute_status = data.get('execute_status', None)
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    schedule_name = data.get('schedule_name')
    system_name = data.get('system_name')
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_timeliness_scheduler_info = GenericCRUD.query_by_conditions(QualityExecute,filters={'rule_type': '及时性检查'},order_by='-created_at')
        if datasource_id:
            quality_timeliness_scheduler_info = GenericCRUD.query_by_conditions(QualityExecute, filters={'database_id': datasource_id,'rule_type':'及时性检查'},order_by='-created_at')
        for quality_timeliness_scheduler in quality_timeliness_scheduler_info:
            datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo, filters={'id': quality_timeliness_scheduler.get('database_id')}, first=True)
            system_info = GenericCRUD.query_by_conditions(BelongSystem, filters={'id': datasource_info.get('belonging_system_id')}, first=True)
            quality_timeliness_scheduler['datasource_type'] = datasource_info.get('database_type')
            quality_timeliness_scheduler['datasource_name'] = datasource_info.get('datasource_name')
            quality_timeliness_scheduler['department'] = system_info.get('department')
            quality_timeliness_scheduler['belonging_department'] = system_info.get('belonging_department')
            quality_timeliness_scheduler['system_name'] = system_info.get('system_name')
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') if start_time else None
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') if end_time else None
        if start_time and end_time:
            quality_timeliness_scheduler_info = [i for i in quality_timeliness_scheduler_info if start_time <= i.get('created_at') <= end_time]
        elif execute_status:
            quality_timeliness_scheduler_info = [i for i in quality_timeliness_scheduler_info if i.get('execute_status') == execute_status]
        elif schedule_name:
            quality_timeliness_scheduler_info = [i for i in quality_timeliness_scheduler_info if i.get('schedule_name').find(schedule_name) != -1]
        elif system_name:
            quality_timeliness_scheduler_info = [i for i in quality_timeliness_scheduler_info if i.get('system_name').find(system_name) != -1]
        result_data = Pagination(quality_timeliness_scheduler_info, page, per_page)
        result['count'] = result_data.total
        result['data'] = result_data.get_items()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/timeliness/scheduler/detail')
def query_timeliness_scheduler_detail():
    data = request.get_json()
    execute_id = data.get('execute_id')
    table_name = data.get('table_name')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page
    }
    try:
        quality_timeliness_detail_info = GenericCRUD.query_by_conditions(QualityTimeliness, filters={'execute_id': execute_id}, order_by='-created_at')
        for quality_timeliness_detail in quality_timeliness_detail_info:
            if quality_timeliness_detail.get('result') == 'success':
                quality_timeliness_detail['execute_status'] = '成功'
                quality_timeliness_detail['log_info'] = '无'
            else:
                quality_timeliness_detail['execute_status'] = '失败'
                quality_timeliness_detail['log_info'] = '失败信息'
        if table_name:
            quality_timeliness_detail_info = [i for i in quality_timeliness_detail_info if i.get('quality_table_name').find(table_name) != -1]
        result_data = Pagination(quality_timeliness_detail_info, page, per_page)
        result['count'] = result_data.total
        result['data'] = result_data.get_items()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/timeliness/latest/execution')
def query_timeliness_latest_execution():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id', None)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_timeliness_scheduler = GenericCRUD.query_by_conditions(QualityExecute,
                                                                            filters={'database_id': datasource_id,
                                                                                     'rule_type': '及时性检查'},
                                                                            order_by='-created_at',first=True)
        if quality_timeliness_scheduler != {}:
            datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo, filters={
                'id': quality_timeliness_scheduler.get('database_id')}, first=True)
            system_info = GenericCRUD.query_by_conditions(BelongSystem,
                                                          filters={'id': datasource_info.get('belonging_system_id')},
                                                          first=True)
            quality_timeliness_scheduler['datasource_type'] = datasource_info.get('database_type')
            quality_timeliness_scheduler['datasource_name'] = datasource_info.get('datasource_name')
            quality_timeliness_scheduler['department'] = system_info.get('department')
            quality_timeliness_scheduler['belonging_department'] = system_info.get('belonging_department')
            quality_timeliness_scheduler['system_name'] = system_info.get('system_name')

            result_data = Pagination([quality_timeliness_scheduler], page, per_page)
        else:
            result_data = Pagination([], page, per_page)
        result['count'] = result_data.total
        result['data'] = result_data.get_items()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/normative/scheduler')
def query_normative_scheduler():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id',None)
    execute_status = data.get('execute_status',None)
    start_time = data.get('start_time',None)
    end_time = data.get('end_time',None)
    schedule_name = data.get('schedule_name',None)
    system_name = data.get('system_name', None)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_normative_scheduler_info = GenericCRUD.query_by_conditions(QualityExecute,filters={'rule_type': '规范性检查'},order_by='-created_at')
        if datasource_id:
            quality_normative_scheduler_info = GenericCRUD.query_by_conditions(QualityExecute, filters={'database_id': datasource_id,'rule_type':'规范性检查'},order_by='-created_at')
        for quality_normative_scheduler in quality_normative_scheduler_info:
            datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo, filters={'id': quality_normative_scheduler.get('database_id')}, first=True)
            system_info = GenericCRUD.query_by_conditions(BelongSystem, filters={'id': datasource_info.get('belonging_system_id')}, first=True)
            quality_normative_scheduler['datasource_name'] = datasource_info.get('datasource_name')
            quality_normative_scheduler['department'] = system_info.get('department')
            quality_normative_scheduler['belonging_department'] = system_info.get('belonging_department')
            quality_normative_scheduler['system_name'] = system_info.get('system_name')

        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') if start_time else None
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') if end_time else None
        if start_time and end_time:
            quality_normative_scheduler_info = [i for i in quality_normative_scheduler_info if i.get('created_at') > start_time and i.get('created_at') < end_time]
        elif execute_status:
            quality_normative_scheduler_info = [i for i in quality_normative_scheduler_info if i.get('execute_status') == execute_status]
        elif schedule_name:
            quality_normative_scheduler_info = [i for i in quality_normative_scheduler_info if i.get('schedule_name').find(schedule_name) != -1]
        elif system_name:
            quality_normative_scheduler_info = [i for i in quality_normative_scheduler_info if i.get('system_name').find(system_name) != -1]
        result_data = Pagination(items=quality_normative_scheduler_info, page=page, per_page=per_page)
        result['data'] = result_data.get_items()
        count = result_data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/normative')
def query_normative():
    data = request.get_json()
    execute_id = data.get('execute_id')
    table_name = data.get('table_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_normative_result = GenericCRUD.query_by_conditions(QualityNormative, filters={'execute_id': execute_id})
        for quality_normative in quality_normative_result:
            table_info = GenericCRUD.query_by_conditions(TableInfo, filters={'id': quality_normative.get('quality_table_id')}, first=True)
            quality_normative['table_name'] = table_info.get('table_name')
        total_no_table_comment = sum([i.get('table_no_comment') for i in quality_normative_result])
        total_no_field_comment = sum([i.get('field_no_comment') for i in quality_normative_result])
        total_field_count = sum([i.get('field_count') for i in quality_normative_result])
        total_no_pk = sum([1 for i in quality_normative_result if i.get('is_have_primary_keys') is False])
        if table_name:
            quality_normative_result = [i for i in quality_normative_result if i.get('table_name').find(table_name) != -1]
        if sort_key:
            quality_normative_result = sorted(quality_normative_result, key=lambda x: x.get(sort_key), reverse=True if order == 'desc' else False)
        result['total_no_table_comment'] = total_no_table_comment
        result['total_no_field_comment'] = total_no_field_comment
        result['total_field_count'] = total_field_count
        result['total_no_pk'] = total_no_pk
        data = Pagination(items=quality_normative_result, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/normative/details')
def query_normative_details():
    data = request.get_json()
    execute_id = data.get('execute_id')
    table_name = data.get('table_name',None)
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    result = {
        'page': page,
        'per_page': per_page,
    }
    if order == 'desc':
        _order = '-{field}'
    else:
        _order = '{field}'
    try:
        quality_normative = GenericCRUD.query_by_conditions(QualityNormative, filters={'execute_id': execute_id},order_by='-created_at')
        if sort_key:
            quality_normative = GenericCRUD.query_by_conditions(QualityNormative, filters={'execute_id': execute_id},
                                                                order_by=_order.format(field=sort_key))
        for _quality_normative in quality_normative:
            _table_name = GenericCRUD.query_by_conditions(TableInfo, filters={'id': _quality_normative.get('quality_table_id')}, first=True).get('table_name')
            _quality_normative['table_name'] = _table_name
        if table_name:
            quality_normative = [i for i in quality_normative if i.get('table_name') == table_name]
        data = Pagination(items=quality_normative, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/normative/latest/execution')
def query_normative_latest_execution():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_normative_scheduler = GenericCRUD.query_by_conditions(QualityExecute, filters={'database_id': datasource_id,'rule_type':'规范性检查'},order_by='-created_at',first=True)
        if quality_normative_scheduler != {}:
            datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo, filters={'id': quality_normative_scheduler.get('database_id')}, first=True)
            system_info = GenericCRUD.query_by_conditions(BelongSystem, filters={'id': datasource_info.get('belonging_system_id')}, first=True)
            quality_normative_scheduler['datasource_name'] = datasource_info.get('datasource_name')
            quality_normative_scheduler['department'] = system_info.get('department')
            quality_normative_scheduler['belonging_department'] = system_info.get('belonging_department')
            quality_normative_scheduler['system_name'] = system_info.get('system_name')
            result_data = Pagination(items=[quality_normative_scheduler], page=page, per_page=per_page)
        else:
            result_data = Pagination(items=[], page=page, per_page=per_page)
        result['data'] = result_data.get_items()
        count = result_data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()


@router.post('/query/table/normative/details')
def query_table_normative_details():
    data = request.get_json()
    quality_table_id = data.get('table_id')
    execute_id = data.get('execute_id')
    database_id = data.get('datasource_id')
    field = data.get('field_name')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_normative_detail = GenericCRUD.query_by_conditions(QualityNormativeDetail,
                                                                   filters={'quality_table_id': quality_table_id, 'execute_id': execute_id,'database_id': database_id}, order_by='-created_at')
        for _quality_normative_detail in quality_normative_detail:
            table_name = GenericCRUD.query_by_conditions(TableInfo, filters={'id': _quality_normative_detail.get('quality_table_id')}, first=True).get('table_name')
            _quality_normative_detail['table_name'] = table_name
            field_name = GenericCRUD.query_by_conditions(FieldHistoryInfo,filters={'id': _quality_normative_detail.get('quality_field_id')}, first=True).get('name')
            _quality_normative_detail['field_name'] = field_name
        if field:
            quality_normative_detail = [i for i in quality_normative_detail if i.get('field_name').find(field) != -1]
        data = Pagination(items=quality_normative_detail, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/quality/rating')
def query_quality_rating():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_name = data.get('datasource_name')
    department = data.get('department')
    system_name = data.get('system_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        datasource_ids = set()
        quality_rating = GenericCRUD.query_by_conditions(QualityReportResult, order_by='-created_at')
        for quality in quality_rating:
            datasource_ids.add(quality.get('database_id'))
        datasource_infos = GenericCRUD.query_by_conditions(DatasourceInfo, conditions=DatasourceInfo.id.in_(datasource_ids))
        for datasource_info in datasource_infos:
            system_info = GenericCRUD.query_by_conditions(BelongSystem,filters={'id':datasource_info.get('belonging_system_id')},first=True)
            quality_rating = GenericCRUD.query_by_conditions(QualityReportResult,filters={'database_id':datasource_info.get('id'),'table_id':None}, order_by='-created_at',first=True)
            datasource_info['execute_id'] = quality_rating.get('execute_id')
            datasource_info['system_name'] = system_info.get('system_name')
            datasource_info['department'] = system_info.get('department')
            datasource_info['belonging_department'] = system_info.get('belonging_department')
            datasource_info['execute_time'] = quality_rating.get('updated_at')
            datasource_info['total'] = quality_rating.get('total')
        if datasource_name:
            datasource_infos = [i for i in datasource_infos if i.get('datasource_name').find(datasource_name) != -1]
        elif department:
            datasource_infos = [i for i in datasource_infos if i.get('department').find(department) != -1]
        elif system_name:
            datasource_infos = [i for i in datasource_infos if i.get('system_name').find(system_name) != -1]
        if sort_key:
            datasource_infos = sorted(
                datasource_infos,
                key=lambda x: (x.get(sort_key) is None, x.get(sort_key)),
                reverse=True if order == 'desc' else False
            )
        data = Pagination(items=datasource_infos, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/quality/rating/update')
def quality_rating_update():
    data = request.get_json()
    execute_id = data.get('execute_id')
    datasource_id = data.get('datasource_id')
    total = data.get('total')
    try:
        quality_rating = GenericCRUD.query_by_conditions(QualityReportResult,filters={'database_id':datasource_id,'execute_id':execute_id,'table_id': None}, order_by='-created_at',first=True)
        GenericCRUD.update(QualityReportResult,id=quality_rating.get('id'),total=total)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/query/quality/rating/table')
def query_quality_rating_table():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id')
    execute_id = data.get('execute_id')
    table_name = data.get('table_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_rating_details = GenericCRUD.query_by_conditions(QualityReportResult,filters={'database_id':datasource_id,'execute_id':execute_id}, order_by='-created_at')
        result_data = []
        for quality_rating in quality_rating_details:
            if quality_rating.get('table_id'):
                table_info = GenericCRUD.query_by_conditions(TableHistoryTemplateInfo,filters={'id':quality_rating.get('table_id')},first=True)
                quality_rating['table_name'] = table_info.get('table_name')
                result_data.append(quality_rating)
        if table_name:
            result_data = [i for i in result_data if i.get('table_name').find(table_name) != -1]
        if sort_key:
            result_data = sorted(
                result_data,
                key=lambda x: (x.get(sort_key) is None, x.get(sort_key)),
                reverse=True if order == 'desc' else False
            )
        data = Pagination(items=result_data, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/query/quality/rating/field')
def query_quality_rating_field():
    data = request.get_json()
    execute_id = data.get('execute_id')
    table_id = data.get('table_id')
    field_name = data.get('field_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        result_data = []
        quality_integrity = GenericCRUD.query_by_conditions(QualityIntegrity, filters={'execute_id': execute_id,
                                                                                       'table_id': table_id,
                                                                                       'execute_log':None})
        for i in quality_integrity:
            rule_info = GenericCRUD.query_by_conditions(Rule,filters={'id':i.get('rule_id')},first=True)
            i['rule_name'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                i['rule_name'] = ''
            i['dimension'] = rule_info.get('dimension')
            i['rule_type'] = rule_info.get('rule_type')
            i['weight'] = rule_info.get('weight')
            i['pass_rate'] = round((i['count']-i['problem_lines']) / i['count'], 2)
            result_data.append(i)
        quality_repeatability = GenericCRUD.query_by_conditions(QualityRepeatability, filters={'execute_id': execute_id,
                                                                                               'table_id': table_id,
                                                                                       'execute_log':None})
        for i in quality_repeatability:
            rule_info = GenericCRUD.query_by_conditions(Rule, filters={'id': i.get('rule_id')}, first=True)
            i['rule_name'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                i['quality_field_name'] = None
            i['dimension'] = rule_info.get('dimension')
            i['rule_type'] = rule_info.get('rule_type')
            i['weight'] = rule_info.get('weight')
            i['pass_rate'] = round((i['count']-i['problem_lines']) / i['count'], 2)
            result_data.append(i)
        quality_accuracy = GenericCRUD.query_by_conditions(QualityAccuracy, filters={'execute_id': execute_id,
                                                                                     'table_id': table_id,
                                                                                       'execute_log':None})
        for i in quality_accuracy:
            rule_info = GenericCRUD.query_by_conditions(Rule, filters={'id': i.get('rule_id')}, first=True)
            i['rule_name'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                i['rule_name'] = ''
            i['dimension'] = rule_info.get('dimension')
            i['rule_type'] = rule_info.get('rule_type')
            i['weight'] = rule_info.get('weight')
            i['pass_rate'] = round((i['count']-i['problem_lines']) / i['count'], 2)
            result_data.append(i)
        quality_consistency = GenericCRUD.query_by_conditions(QualityConsistency, filters={'execute_id': execute_id,
                                                                                           'table_id': table_id,
                                                                                       'execute_log':None})
        for i in quality_consistency:
            rule_info = GenericCRUD.query_by_conditions(Rule,filters={'id':i.get('rule_id')},first=True)
            i['rule_name'] = rule_info.get('rule_code')
            if rule_info.get('dimension') == 'table':
                i['rule_name'] = ''
            i['dimension'] = rule_info.get('dimension')
            i['rule_type'] = rule_info.get('rule_type')
            i['weight'] = rule_info.get('weight')
            i['pass_rate'] = round((i['count']-i['problem_lines']) / i['count'], 2)
            result_data.append(i)
        if field_name:
            result_data = [i for i in result_data if i.get('field_name') == field_name]
        if sort_key:
            result_data = sorted(
                result_data,
                key=lambda x: (x.get(sort_key) is None, x.get(sort_key)),
                reverse=True if order == 'desc' else False
            )
        data = Pagination(items=result_data, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/quality/rating/field/update')
def quality_rating_field_update():
    data = request.get_json()
    rule_type = data.get('rule_type')
    id = data.get('id')
    total = data.get('total')
    try:
        if rule_type == '数据完整性':
            model_class = QualityIntegrity
        elif rule_type == '数据一致性':
            model_class = QualityConsistency
        elif rule_type == '数据准确性':
            model_class = QualityAccuracy
        elif rule_type == '数据唯一性':
            model_class = QualityRepeatability
        else:
            return ErrorResponse(error_data='rule_type参数错误').to_response()
        GenericCRUD.update(model_class, id=id, score=total)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/query/quality/rating/details')
def query_quality_rating_details():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_id = data.get('datasource_id')
    datasource_name = data.get('datasource_name')
    system_name = data.get('system_name')
    order = data.get('order','desc')
    sort_key = data.get('sort_key')
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        quality_rating_details = GenericCRUD.query_by_conditions(QualityReportResult,filters={'database_id':datasource_id,'table_id':None}, order_by='-created_at')
        for quality_rating in quality_rating_details:
            datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo,filters={'id':quality_rating.get('database_id')},first=True)
            system_info = GenericCRUD.query_by_conditions(BelongSystem,filters={'id':datasource_info.get('belonging_system_id')},first=True)
            quality_rating['system_name'] = system_info.get('system_name')
            quality_rating['department'] = system_info.get('department')
            quality_rating['belonging_department'] = system_info.get('belonging_department')
            quality_rating['datasource_name'] = datasource_info.get('datasource_name')
            quality_rating['datasource_type'] = datasource_info.get('database_type')
        if datasource_name:
            quality_rating_details = [i for i in quality_rating_details if i.get('datasource_name').find(datasource_name) != -1]
        if system_name:
            quality_rating_details = [i for i in quality_rating_details if i.get('system_name').find(system_name) != -1]
        if sort_key:
            quality_rating_details = sorted(
                quality_rating_details,
                key=lambda x: (x.get(sort_key) is None, x.get(sort_key)),
                reverse=True if order == 'desc' else False
            )
        data = Pagination(items=quality_rating_details, page=page, per_page=per_page)
        result['data'] = data.get_items()
        count = data.total
        result['count'] = count
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/configure/timeliness')
def configure_timeliness():
    data = request.get_json()
    table_id = data.get('table_id')
    datasource_id = data.get('datasource_id')
    up_cycle = data.get('up_cycle')
    try:
        configure_timeliness = GenericCRUD.query_by_conditions(ConfigureTimelinessInfo,filters={'table_id':table_id,'datasource_id':datasource_id},first=True)
        if configure_timeliness:
            GenericCRUD.update(ConfigureTimelinessInfo, id=configure_timeliness.get('id'), up_cycle=up_cycle)
        else:
            GenericCRUD.create(ConfigureTimelinessInfo, table_id=table_id, datasource_id=datasource_id, up_cycle=up_cycle)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()

@router.post('/configure/timeliness/batch')
def configure_timeliness_batch():
    data = request.get_json()
    table_id = data.get('table_id',[])
    datasource_id = data.get('datasource_id')
    up_cycle = data.get('up_cycle')
    try:
        for i in table_id:
            configure_timeliness = GenericCRUD.query_by_conditions(ConfigureTimelinessInfo,filters={'table_id':i,'datasource_id':datasource_id},first=True)
            if configure_timeliness:
                GenericCRUD.update(ConfigureTimelinessInfo, id=configure_timeliness.get('id'), up_cycle=up_cycle)
            else:
                GenericCRUD.create(ConfigureTimelinessInfo, table_id=i, datasource_id=datasource_id, up_cycle=up_cycle)
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse().to_response()
