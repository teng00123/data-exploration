from flask import Blueprint, jsonify, request
from backend.database.exploration_model import BelongSystem, TableHistoryTemplateInfo, TableInfo, FieldInfo, \
    DatasourceInfo
from backend.database.db_push import DbPushTable, DbPushField
from backend.database.directory import DataDirectory, DataDirectoryItem
from backend.database.schedule_info import ScheduleInfo, ScheduleExecute
from backend.database.sys_model import SysDept, DeptBatch, DataType, ServiceObject, SysUser
from backend.utils import custom_jwt_required
from sqlalchemy import func,or_

report_froms_bp = Blueprint('report_forms', __name__)


@report_froms_bp.route('/query/v1', methods=['POST'])
@custom_jwt_required
def query_report_forms_v1():
    data_total = sum([int(i.data_zie) for i in DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).all() if i.data_zie !=None])
    data_resources_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).count()
    data_resources_item_total = DataDirectoryItem.query.join(DataDirectory,
                                                             DataDirectoryItem.data_directory_id == DataDirectory.id).filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).count()
    no_dept_ids = [4,1851507096929443842,1861578281075449858,1856162650240790529]
    system_total = BelongSystem.query.filter(BelongSystem.department_id.not_in (no_dept_ids)).count()
    system_completion = BelongSystem.query.filter(BelongSystem.belonging_department != "").filter(BelongSystem.department_id.not_in (no_dept_ids)).count()
    system_completion_rate = system_completion / system_total * 100
    dept_total = SysDept.query.filter_by(parent_id='1', del_flag='0').filter(SysDept.dept_id.not_in(no_dept_ids)).count()
    table_total = TableInfo.query.filter_by(is_delete=False).join(DatasourceInfo,
                                                                      DatasourceInfo.id == TableInfo.datasource_id).join(
            BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.department_id.not_in(no_dept_ids)).count()
    field_total = FieldInfo.query.filter_by(is_delete=False).join(TableInfo,
                                                                      TableInfo.id == FieldInfo.table_info_id).filter_by(
            is_delete=False).join(DatasourceInfo, DatasourceInfo.id == TableInfo.datasource_id).join(BelongSystem,
                                                                                                     BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.department_id.not_in(no_dept_ids)).count()
    dept_ips = [i.department_id for i in ScheduleInfo.query.filter(ScheduleInfo.department_id != 4).with_entities(
        ScheduleInfo.department_id,
        func.count(ScheduleInfo.id).label('count')
    ).group_by(ScheduleInfo.department_id).all()]
    dept_ip = set()
    for i in dept_ips:
        dept = SysDept.query.filter_by(dept_id=i).first()
        if dept.parent_id == 1:
            dept_ip.add(i)
        else:
            dept_ip.add(dept.parent_id)
    dept_completion = len(dept_ip) + 21
    dept_completion_rate = dept_completion / dept_total * 100
    data_storage = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).with_entities(
        func.sum(DataDirectory.data_storage_capacity)).scalar()
    data_storage = int(data_storage) if data_storage else 0
    data = {
        "data_total": data_total,
        "data_resources_total": data_resources_total,
        "system_total": system_total,
        "data_resources_item_total": data_resources_item_total,
        "dept_total": dept_total,
        "system_completion_rate": system_completion_rate,
        "table_total": table_total,
        "field_total": field_total,
        "data_storage": data_storage / 1024,
        "dept_completion": dept_completion,
        "dept_completion_rate": dept_completion_rate
    }
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/query/v2', methods=['POST'])
@custom_jwt_required
def query_report_forms_v2():
    data = request.get_json()
    dept_id = data.get('dept_id')
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    if sys_dept.parent_id != 1:
        dept_id = sys_dept.parent_id
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag='0').all()]
    dept_ids.append(dept_id)
    system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).count()
    system_completion = BelongSystem.query.join(DatasourceInfo,
                                                DatasourceInfo.belonging_system_id == BelongSystem.id).filter(
        BelongSystem.department_id.in_(dept_ids)).group_by(BelongSystem.id).count()
    system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).all()]
    datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
        DataDirectory.system_id.in_(system_ids)).count()
    data_resources_item_total = DataDirectoryItem.query.join(DataDirectory,
                                                             DataDirectoryItem.data_directory_id == DataDirectory.id).filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(DataDirectory.system_id.in_(system_ids)).count()
    datasource_status_1_total = DataDirectory.query.filter_by(status='1', build_directory=True).filter(
        DataDirectory.system_id.in_(system_ids)).count()
    datasource_status_2_total = DataDirectory.query.filter_by(build_directory=False).filter(
        DataDirectory.system_id.in_(system_ids)).count()
    datasource_status_3_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
        DataDirectory.system_id.in_(system_ids)).count()
    database_total = DatasourceInfo.query.filter(DatasourceInfo.belonging_system_id.in_(system_ids)).count()
    table_total = TableInfo.query.filter_by(is_delete=False).join(DatasourceInfo,
                                                                  DatasourceInfo.id == TableInfo.datasource_id).filter(
        DatasourceInfo.belonging_system_id.in_(system_ids)).count()
    data_storge = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
        DataDirectory.system_id.in_(system_ids)).with_entities(func.sum(DataDirectory.data_storage_capacity)).scalar()
    data_storge = int(data_storge) if data_storge else 0
    fail_conn = ScheduleExecute.query.filter(ScheduleExecute.failure_reason.like("%password%")).join(ScheduleInfo,
                                                                                                     ScheduleInfo.id == ScheduleExecute.schedule_id).filter(
        ScheduleInfo.department_id.in_(dept_ids)).count()
    data_total = sum([int(i.data_zie) for i in DataDirectory.query.filter_by(build_directory=True).filter(
        or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                            BelongSystem.id == DataDirectory.system_id).filter(
        BelongSystem.department_id.in_(dept_ids)).all() if i.data_zie != None])
    data = {
        "system_total": system_total,
        "system_completion": system_completion,
        "datasource_total": datasource_total,
        "datasource_item_total": data_resources_item_total,
        "datasource_status_1_total": datasource_status_1_total,
        "datasource_status_2_total": datasource_status_2_total,
        "datasource_status_3_total": datasource_status_3_total,
        "database_total": database_total,
        "table_total": table_total,
        "data_storge": round(data_storge / 1024,2),
        "fail_conn": fail_conn,
        "data_total":data_total
    }
    return jsonify({"code": 200, "data": data})


@report_froms_bp.route('/batch/query/v1', methods=['POST'])
@custom_jwt_required
def batch_query_v1():
    batch_names_info = DeptBatch.query.filter_by(batch_enable=True).all()
    batch_names = [batch.batch_name for batch in batch_names_info]
    data = {'data': []}
    for batch_name in batch_names:
        dept_total = SysDept.query.filter_by(batch_name=batch_name, del_flag='0').count()
        dept_ids = [i.dept_id for i in SysDept.query.filter_by(batch_name=batch_name, del_flag='0').all()]
        dept_info = [i.dept_id for i in
                     SysDept.query.filter_by(del_flag='0').filter(SysDept.parent_id.in_(dept_ids)).all()]
        result_ids = set(dept_ids).union(set(dept_info))
        system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(result_ids)).count()
        system_completion = BelongSystem.query.filter(BelongSystem.belonging_department != "").filter(BelongSystem.department_id.in_(result_ids)).count()
        table_total = TableInfo.query.filter_by(is_delete=False).join(DatasourceInfo,
                                                                      DatasourceInfo.id == TableInfo.datasource_id).join(
            BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.department_id.in_(result_ids)).count()+ DbPushTable.query.join(BelongSystem,BelongSystem.id==DbPushTable.system_id).filter(
            BelongSystem.department_id.in_(result_ids)).count()
        field_total = FieldInfo.query.filter_by(is_delete=False).join(TableInfo,
                                                                      TableInfo.id == FieldInfo.table_info_id).filter_by(
            is_delete=False).join(DatasourceInfo, DatasourceInfo.id == TableInfo.datasource_id).join(BelongSystem,
                                                                                                     BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.department_id.in_(result_ids)).count()+ DbPushField.query.join(DbPushTable,DbPushTable.id==DbPushField.table_id).join(BelongSystem,BelongSystem.id==DbPushTable.system_id).filter(
            BelongSystem.department_id.in_(result_ids)).count()
        data_total = sum([int(i.data_zie) for i in DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                    BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(result_ids)).all() if i.data_zie != None])
        data_storage = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                      BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(result_ids)).with_entities(
            func.sum(DataDirectory.data_storage_capacity)).scalar()
        data_storage = int(data_storage) if data_storage else 0
        data['data'].append({
            'batch_name': batch_name,
            "dept_total": dept_total,
            "system_completion":system_completion,
            "system_total": system_total,
            "table_total": table_total,
            "field_total": field_total,
            "data_total": data_total,
            "data_storage": data_storage / 1024
        })
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/dept/system/query/v1', methods=['POST'])
@custom_jwt_required
def dept_query_v1():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('pageSize', 10)
    dept_name = data.get('dept_name', None)
    sort_key = data.get('sort_key', None)
    order = data.get('order', 'asc')
    if not dept_name:
        query = SysDept.query.filter_by(parent_id='1', del_flag='0').filter(SysDept.dept_id != 4)
    else:
        query = SysDept.query.filter_by(del_flag='0').filter(SysDept.dept_name.in_(dept_name)).filter(
            SysDept.dept_id != 4)
    dept_info_list = query.all()
    data = {
        'page': page,
        'per_page': per_page,
        'count': query.count(),
    }
    sorted_data = []
    for dept_info in dept_info_list:
        dept_ids_list = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_info.dept_id, del_flag='0').all()]
        dept_ids_list.append(dept_info.dept_id)
        system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids_list)).count()
        system_completion = BelongSystem.query.filter(BelongSystem.belonging_department != "").filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        table_total = TableInfo.query.filter_by(is_delete=False).join(DatasourceInfo,
                                                                      DatasourceInfo.id == TableInfo.datasource_id).join(
            BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count() + DbPushTable.query.join(BelongSystem,BelongSystem.id==DbPushTable.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        # field_total = FieldInfo.query.filter_by(is_delete=False).join(TableInfo,
        #                                                               TableInfo.id == FieldInfo.table_info_id).filter_by(
        #     is_delete=False).join(DatasourceInfo, DatasourceInfo.id == TableInfo.datasource_id).join(BelongSystem,
        #                                                                                              BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
        #     BelongSystem.department_id.in_(dept_ids_list)).count() + DbPushField.query.join(DbPushTable,DbPushTable.id==DbPushField.table_id).join(BelongSystem,BelongSystem.id==DbPushTable.system_id).filter(
        #     BelongSystem.department_id.in_(dept_ids_list)).count()
        field_total = DataDirectoryItem.query.join(DataDirectory,DataDirectoryItem.data_directory_id==DataDirectory.id).filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                    BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        data_total = sum([int(i.data_zie) for i in DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                    BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).all() if i.data_zie != None])
        data_total = int(data_total) if data_total else 0
        data_storage = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                      BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).with_entities(
            func.sum(DataDirectory.data_storage_capacity)).scalar()
        data_storage = int(data_storage) if data_storage else 0
        sorted_data.append({
            'dept_name': dept_info.dept_name,
            'system_total': system_total,
            'system_completion': system_completion,
            'table_total': table_total,
            'field_total': field_total,
            'data_total': data_total,
            'data_storage': data_storage / 1024
        })
    # Calculate the start and end index for the current page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    if sort_key:
        sorted_data = sorted(sorted_data, key=lambda x: x[sort_key], reverse=False if order == 'asc' else True)
    data['data'] = sorted_data[start_index:end_index]
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/dept/datasource/query/v1', methods=['POST'])
@custom_jwt_required
def dept_datasource_query_v1():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('pageSize', 10)
    dept_name = data.get('dept_name', None)
    sort_key = data.get('sort_key', None)
    order = data.get('order', 'asc')
    if not dept_name:
        query = SysDept.query.filter_by(parent_id='1', del_flag='0').filter(SysDept.dept_id != 4)
    else:
        query = SysDept.query.filter_by(del_flag='0').filter(SysDept.dept_name.in_(dept_name)).filter(
            SysDept.dept_id != 4)
    dept_info_list = query.all()
    data = {
        'page': page,
        'per_page': per_page,
        'count': query.count(),
    }
    sorted_data = []
    for dept_info in dept_info_list:
        dept_ids_list = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_info.dept_id, del_flag='0').all()]
        dept_ids_list.append(dept_info.dept_id)
        datasource_status_1_total = DataDirectory.query.filter_by(status='1', build_directory=True).join(BelongSystem,
                                                                                                         BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        datasource_status_2_total = DataDirectory.query.filter_by(build_directory=False).join(BelongSystem,
                                                                                              BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        datasource_status_3_total = DataDirectory.query.filter_by(status='3', build_directory=True).join(BelongSystem,
                                                                                                         BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        datasource_status_4_total = DataDirectory.query.filter_by(status='2', build_directory=True).join(BelongSystem,
                                                                                                         BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        table_total = TableInfo.query.filter_by(is_delete=False).join(DatasourceInfo,
                                                                      DatasourceInfo.id == TableInfo.datasource_id).join(
            BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        result_table_total = DbPushTable.query.join(SysUser,SysUser.user_id == DbPushTable.create_id).filter(
            SysUser.dept_id.in_(dept_ids_list)).count()
        sorted_data.append({
            'dept_name': dept_info.dept_name,
            'datasource_status_1_total': datasource_status_1_total,
            'datasource_status_2_total': datasource_status_2_total,
            'datasource_status_3_total': datasource_status_3_total,
            'datasource_status_4_total':datasource_status_4_total,
            'result_table_total':result_table_total,
            'table_total': table_total,
        })
    # Calculate the start and end index for the current page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    if sort_key:
        sorted_data = sorted(sorted_data, key=lambda x: x[sort_key], reverse=False if order == 'asc' else True)
    data['data'] = sorted_data[start_index:end_index]
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/exploration/situation', methods=['POST'])
@custom_jwt_required
def exploration_situation():
    data = request.get_json()
    dept_id = data.get('dept_id')
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    if sys_dept.parent_id != 1:
        dept_id = sys_dept.parent_id
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag='0').all()]
    dept_ids.append(dept_id)
    schedule_total = ScheduleInfo.query.filter(ScheduleInfo.department_id.in_(dept_ids)).count()
    schedule_executed_total = ScheduleExecute.query.join(ScheduleInfo,
                                                         ScheduleInfo.id == ScheduleExecute.schedule_id).filter(
        ScheduleInfo.department_id.in_(dept_ids)).count()
    table_total = TableInfo.query.filter_by(is_delete=False).join(DatasourceInfo,
                                                                  DatasourceInfo.id == TableInfo.datasource_id).join(
        BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
        BelongSystem.department_id.in_(dept_ids)).count()
    field_total = FieldInfo.query.filter_by(is_delete=False).join(TableInfo,
                                                                  TableInfo.id == FieldInfo.table_info_id).filter_by(
        is_delete=False).join(DatasourceInfo, DatasourceInfo.id == TableInfo.datasource_id).join(BelongSystem,
                                                                                                 BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
        BelongSystem.department_id.in_(dept_ids)).count()

    data = {
        'schedule_total': schedule_total,
        'schedule_executed_total': schedule_executed_total,
        'table_total': table_total,
        'field_total': field_total
    }
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/schedule/execute/situation', methods=['POST'])
@custom_jwt_required
def schedule_execute_situation():
    data = request.get_json()
    dept_id = data.get('dept_id')
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    if sys_dept.parent_id != 1:
        dept_id = sys_dept.parent_id
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag='0').all()]
    dept_ids.append(dept_id)
    schedule_execute_success_total = ScheduleExecute.query.join(ScheduleInfo,
                                                                ScheduleInfo.id == ScheduleExecute.schedule_id).filter(
        ScheduleInfo.department_id.in_(dept_ids), ScheduleExecute.schedule_status == '成功').count()
    schedule_execute_fail_total = ScheduleExecute.query.join(ScheduleInfo,
                                                             ScheduleInfo.id == ScheduleExecute.schedule_id).filter(
        ScheduleInfo.department_id.in_(dept_ids), ScheduleExecute.schedule_status == '失败').count()
    data = {
        'schedule_execute_success_total': schedule_execute_success_total,
        'schedule_execute_fail_total': schedule_execute_fail_total
    }
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/system/classification/query', methods=['POST'])
@custom_jwt_required
def system_classification_query():
    data = request.get_json()
    dept_id = data.get('dept_id')
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    if sys_dept.parent_id != 1:
        dept_id = sys_dept.parent_id
    type = data.get('type')
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag='0').all()]
    dept_ids.append(dept_id)
    total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).count()
    _datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                      BelongSystem.id == DataDirectory.system_id).filter(BelongSystem.department_id.in_(dept_ids)).count()
    data = {'data': [],'total': total}
    if type == "1":
        system_type = ['基础设施', '数据系统', '业务系统', '政务服务系统', '其他']
        for i in system_type:
            system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.system_type.like(f'%{i}%')).count()
            system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.system_type.like(f'%{i}%')).all()]
            datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                              BelongSystem.id == DataDirectory.system_id).filter(
                BelongSystem.id.in_(system_ids)).count()
            data['data'].append(
                {
                    'name': i,
                    'system': system_total,
                    'datasource': datasource_total / _datasource_total * 100 if _datasource_total != 0 else 0
                }
            )
        return jsonify({'code': 200, 'data': data})
    elif type == "2":
        using_objects = ['企业', '社会公众', '部门内部']
        for i in using_objects:
            system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.service_object.like(f'%{i}%')).count()
            system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.service_object.like(f'%{i}%')).all()]
            datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                              BelongSystem.id == DataDirectory.system_id).filter(
                BelongSystem.id.in_(system_ids)).count()
            data['data'].append(
                {
                    'name': i,
                    'system': system_total,
                    'datasource': datasource_total / _datasource_total * 100 if _datasource_total != 0 else 0
                }
            )
        return jsonify({'code': 200, 'data': data})

    elif type == "3":
        construction_method = ['本级建设(或部署)政务信息系统', '国家部委部署系统', '其他']
        for i in construction_method:
            system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.build_method == i).count()
            system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.build_method == i).all()]
            datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                              BelongSystem.id == DataDirectory.system_id).filter(
                BelongSystem.id.in_(system_ids)).count()
            data['data'].append(
                {
                    'name': i,
                    'system': system_total,
                    'datasource': datasource_total / _datasource_total * 100 if _datasource_total != 0 else 0
                }
            )
        return jsonify({'code': 200, 'data': data})

    elif type == "4":
        networks = ['互联网', '电子政务外网', '电子政务内网', '行业专网', '电子政务外网和互联网']
        for i in networks:
            system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.network == i).count()
            system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.network == i).all()]
            datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                              BelongSystem.id == DataDirectory.system_id).filter(
                BelongSystem.id.in_(system_ids)).count()
            data['data'].append(
                {
                    'name': i,
                    'system': system_total,
                    'datasource':datasource_total / _datasource_total * 100 if _datasource_total != 0 else 0
                }
            )
        return jsonify({'code': 200, 'data': data})

    elif type == "5":
        run_status = ['在建', '在用', '停用']
        for i in run_status:
            system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.run_status == i).count()
            system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).filter(
                BelongSystem.run_status == i).all()]
            datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                              BelongSystem.id == DataDirectory.system_id).filter(
                BelongSystem.id.in_(system_ids)).count()
            data['data'].append(
                {
                    'name': i,
                    'system': system_total,
                    'datasource': datasource_total / _datasource_total * 100 if _datasource_total != 0 else 0
                }
            )
        return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/datasource/classification/query', methods=['POST'])
@custom_jwt_required
def datasource_classification_query():
    data = request.get_json()
    dept_id = data.get('dept_id')
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    if sys_dept.parent_id != 1:
        dept_id = sys_dept.parent_id
    type = data.get('type')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag='0').all()]
    dept_ids.append(dept_id)
    system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).all()]
    data = {'data': [], 'page': page, 'per_page': per_page}
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    if type == "1":
        ywy_infos = DataType.query.filter_by(type="1").all()
        _data = []
        for ywy_info in ywy_infos:
            _data.append(
                {
                    'name': ywy_info.name,
                    'count': DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
                        DataDirectory.ywy_name.like(f"%{ywy_info.name}%")).join(BelongSystem,
                                                                                BelongSystem.id == DataDirectory.system_id).filter(
                        BelongSystem.id.in_(system_ids)).count()
                }
            )
        _data = sorted(_data, key=lambda x: x['count'], reverse=True)
        data['data'] = _data[start_index:end_index]
        data['count'] = len(ywy_infos)
        return jsonify({'code': 200, 'data': data})
    elif type == "2":
        zty_infos = DataType.query.filter_by(type="2").all()
        _data = []
        for zty_info in zty_infos:
            _data.append(
                {
                    'name': zty_info.name,
                    'count': DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
                        DataDirectory.zty_name.like(f"%{zty_info.name}%")).join(BelongSystem,
                                                                                BelongSystem.id == DataDirectory.system_id).filter(
                        BelongSystem.id.in_(system_ids)).count()
                }
            )
        _data = sorted(_data, key=lambda x: x['count'], reverse=True)
        data['data'] = _data[start_index:end_index]
        data['count'] = len(zty_infos)
        return jsonify({'code': 200, 'data': data})
    elif type == "3":
        service_infos = ServiceObject.query.all()
        _data = []
        for service_info in service_infos:
            _data.append(
                {
                    'name': service_info.name,
                    'count': DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
                        DataDirectory.ydx_name == service_info.name).join(BelongSystem,
                                                                          BelongSystem.id == DataDirectory.system_id).filter(
                        BelongSystem.id.in_(system_ids)).count()
                }
            )
        _data = sorted(_data, key=lambda x: x['count'], reverse=True)
        data['data'] = _data[start_index:end_index]
        data['count'] = len(service_infos)
        return jsonify({'code': 200, 'data': data})
    elif type == "4":
        update_cycle = ["其他", "实时", "每周", "每日", "每季度", "每月", "每年"]
        for cycle in update_cycle:
            data['data'].append(
                {
                    'name': cycle,
                    'count': DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(DataDirectory.up_cycle == cycle).join(
                        BelongSystem, BelongSystem.id == DataDirectory.system_id).filter(
                        BelongSystem.id.in_(system_ids)).count()
                }
            )
        return jsonify({'code': 200, 'data': data})
    elif type == "5":
        data_processing = ["原始数据", "融合数据", "统计数据", "标签数据", "脱敏数据"]
        for processing in data_processing:
            data['data'].append(
                {
                    'name': processing,
                    'count': DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
                        DataDirectory.data_processing == processing).join(BelongSystem,
                                                                          BelongSystem.id == DataDirectory.system_id).filter(
                        BelongSystem.id.in_(system_ids)).count()
                }
            )
        return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/dept/batch/query', methods=['POST'])
@custom_jwt_required
def dept_batch_query():
    batch_names_info = DeptBatch.query.filter_by(batch_enable=True).all()
    batch_names = [batch.batch_name for batch in batch_names_info]
    data = {}
    for batch_name in batch_names:
        data[batch_name] = [i.dept_name for i in SysDept.query.filter_by(batch_name=batch_name).all()]
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/fail/database/query', methods=['POST'])
@custom_jwt_required
def fail_database_query():
    data = request.get_json()
    dept_id = data.get('dept_id')
    database_name = data.get('database_name', None)
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    if sys_dept.parent_id != 1:
        dept_id = sys_dept.parent_id
    page = data.get('page')
    per_page = data.get('per_page')
    start_index = (page - 1) * per_page
    end_index = page * per_page
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag='0').all()]
    dept_ids.append(dept_id)
    schedule_execute_infos = ScheduleExecute.query.filter(ScheduleExecute.failure_reason.like("%password%")).join(
        ScheduleInfo, ScheduleInfo.id == ScheduleExecute.schedule_id).filter(
        ScheduleInfo.department_id.in_(dept_ids)).order_by(ScheduleExecute.schedule_time.desc()).all()
    if database_name:
        schedule_execute_infos = ScheduleExecute.query.filter(ScheduleExecute.failure_reason.like("%password%")).join(
            ScheduleInfo, ScheduleInfo.id == ScheduleExecute.schedule_id).filter(
            ScheduleInfo.department_id.in_(dept_ids)).join(DatasourceInfo,
                                                           DatasourceInfo.id == ScheduleExecute.datasource_id).filter(
            DatasourceInfo.datasource_name == database_name
        ).order_by(ScheduleExecute.schedule_time.desc()).all()

    data = {
        'page': page,
        'per_page': per_page,
        'count': len(schedule_execute_infos),
        'data': []
    }
    _data = []
    for schedule_execute_info in schedule_execute_infos:
        database_name = DatasourceInfo.query.filter_by(id=schedule_execute_info.datasource_id).first().datasource_name
        fail_time = schedule_execute_info.schedule_time
        _data.append({
            'database_name': database_name,
            'fail_time': fail_time
        })
    data['data'] = _data[start_index:end_index]
    return jsonify({'code': 200, 'data': data})


@report_froms_bp.route('/database/query', methods=['POST'])
@custom_jwt_required
def database_query():
    data = request.get_json()
    user_id = data.get('user_id')
    data = {'data': []}
    database_names = [i.datasource_name for i in DatasourceInfo.query.filter_by(create_id=user_id).all()]
    data['data'] = database_names
    return jsonify({'code': 200, 'data': data})
