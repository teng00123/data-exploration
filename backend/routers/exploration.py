import copy
import json
import random
from datetime import datetime, timedelta
from os import abort

import jwt
import pandas as pd
from flask import Blueprint, jsonify, request, send_file, Response
from backend.utils import custom_jwt_required,record_user_operation
from backend.config import config
from backend.database.sys_model import SysDept, SysUser, SysUserRole, SysRole
from backend.database.exploration_model import TableInfo, FieldInfo, DatabaseChangeLog, \
    DatasourceInfo, BelongSystem, TableHistoryInfo, FieldHistoryInfo, DataResources, DataResourcesAuth, \
    DataResourcesDownloadLog, TableHistoryTemplateInfo
from backend.database.schedule_info import ScheduleInfo, ScheduleExecute
from backend.utils import hide_middle_digits,encrypt_password
from backend.config import scheduler, db
from sqlalchemy import create_engine, desc, and_, or_
import uuid
import urllib.parse
import dmPython
from backend.config import r
import os
import logging

exploration_bp = Blueprint('exploration', __name__)


@exploration_bp.route('/create/belong_system', methods=['POST'])
@custom_jwt_required
def create_belong_system():
    data = request.get_json()
    system_info = BelongSystem(
        id=random.randint(10 ** 15, 10 ** 16 - 1),
        system_name=data.get('system_name'),
        department=data.get('department'),
        belonging_department=data.get('belonging_department').get('dept_name'),
        system_summary=data.get('system_summary'),
        run_status=data.get('run_status'),
        network=','.join(data.get('network')),
        build_unit=data.get('build_unit'),
        construction_unit=data.get('construction_unit'),
        service_object=','.join(data.get('service_object')),
        build_method=data.get('build_method'),
        system_type=','.join(data.get('system_type')),
        investment_total=data.get('investment_total'),
        funds_source=','.join(data.get('funds_source')),
        devops_expenses=data.get('devops_expenses'),
        person=data.get('person'),
        phone=data.get('phone'),
        notes=data.get('notes'),
        create_id=data.get('userId'),
        department_id=data.get('belonging_department').get('dept_id')
    )
    db.session.add(system_info)
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/query/belong_system', methods=['GET'])
@custom_jwt_required
def query_belong_system():
    dept_id = request.args.get('deptId')
    user_id = request.args.get('userId')
    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=user_id).first()
    if sys_role.role_id in (1, 1855189077904728066, 1855189303667335169):
        ids_list = [sys_dept.dept_id for sys_dept in SysDept.query.all()]
    elif sys_role.role_id == 1855188956748062721:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id != 1:
            ancestors = sys_dept.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            sys_dept = SysDept.query.filter(and_(
                SysDept.dept_id.in_(ancestors),
                SysDept.parent_id == 1
            )).first()
        _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
        ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
        ids_list.append(sys_dept.dept_id)
    else:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        ids_list = [dept_id, sys_dept.parent_id]
    query = BelongSystem.query.filter(BelongSystem.department_id.in_(ids_list))
    belong_system_infos = query.all()
    belong_system_info_list = [belong_system_info.__dict__ for belong_system_info in belong_system_infos]
    belong_system_info_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                               belong_system_info_list]
    return jsonify({'code': 200, 'data': belong_system_info_list})


@exploration_bp.route('/query/filter/belong_system', methods=['POST'])
@custom_jwt_required
def query_filter_belong_system():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 999999)
    system_name = data.get('system_name', None)
    belonging_department = data.get('belonging_department', None)
    dept_id = data.get('deptId', None)
    user_id = data.get('userId', None)
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=user_id).first()
    if sys_role.role_id in (1, 1855189077904728066, 1855189303667335169):
        ids_list = [sys_dept.dept_id for sys_dept in SysDept.query.all()]
    elif sys_role.role_id == 1855188956748062721:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id != 1:
            ancestors = sys_dept.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            sys_dept = SysDept.query.filter(and_(
                SysDept.dept_id.in_(ancestors),
                SysDept.parent_id == 1
            )).first()
        _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
        ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
        ids_list.append(sys_dept.dept_id)
    else:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        ids_list = [dept_id,sys_dept.parent_id]
    query = BelongSystem.query.filter(
        and_(
            BelongSystem.department_id.in_(ids_list),
        )
    )
    if system_name:
        query = BelongSystem.query.filter(
            and_(
                BelongSystem.system_name.like(f"%{system_name}%"),
            )
        ).filter(
            and_(
                BelongSystem.department_id.in_(ids_list),
            )
        )
    if belonging_department:
        sys_dept = SysDept.query.filter_by(dept_id=data.get('belonging_department')).first()
        if sys_dept.parent_id == 1:
            _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
            id_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
            id_list.append(sys_dept.dept_id)
        else:
            id_list = [sys_dept.dept_id]
        ids_list = list(set(ids_list) & set(id_list))
        query = BelongSystem.query.filter(
            and_(
                BelongSystem.department_id.in_(ids_list),
            )
        )

    if system_name and belonging_department:
        query = BelongSystem.query.filter(
            and_(
                BelongSystem.system_name.like(f"%{system_name}%"),
            )
        ).filter(
            and_(
                BelongSystem.department_id.in_(ids_list),
            )
        )

    count = query.count()
    belong_system_infos = query.order_by(BelongSystem.update_time.desc()).paginate(page=page, per_page=per_page).items
    belong_system_info_list = []
    for belong_system_info in belong_system_infos:
        belong_system_dict = belong_system_info.__dict__
        datasource_count = DatasourceInfo.query.filter_by(belonging_system_id=belong_system_dict.get('id'),
                                                          belonging_system_department_id=belong_system_dict.get(
                                                              'belonging_system_department_id')).count()
        belong_system_dict['id'] = str(belong_system_dict.get('id'))
        belong_system_dict['department_id'] = str(belong_system_dict.get('department_id'))
        belong_system_dict['network'] = belong_system_dict.get('network').split(',') if belong_system_dict.get('network') else []
        belong_system_dict['service_object'] = belong_system_dict.get('service_object').split(',') if belong_system_dict.get('service_object') else []
        belong_system_dict['system_type'] = belong_system_dict.get('system_type').split(',') if belong_system_dict.get('system_type') else []
        belong_system_dict['funds_source'] = belong_system_dict.get('funds_source').split(',') if belong_system_dict.get('funds_source') else []
        belong_system_dict['datasource_count'] = datasource_count
        belong_system_dict['systemName'] = belong_system_dict.get('system_name')
        belong_system_dict['systemId'] = str(belong_system_dict.get('id'))
        belong_system_info_list.append(belong_system_dict)
    belong_system_info_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                               belong_system_info_list]
    data = {
        'data': belong_system_info_list,
        'count': count,
        'page': page,
        'per_page': per_page
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/update/belong_system', methods=['POST'])
@custom_jwt_required
def update_belong_system():
    data = request.get_json()
    belong_system_info = BelongSystem.query.filter_by(id=data.get('id')).first()
    belong_system_info.system_name = data.get('system_name')
    belong_system_info.belonging_department = data.get('belonging_department').get('dept_name')
    belong_system_info.system_summary = data.get('system_summary')
    belong_system_info.run_status = data.get('run_status')
    belong_system_info.network = ','.join(data.get('network'))
    belong_system_info.build_unit = data.get('build_unit')
    belong_system_info.construction_unit = data.get('construction_unit')
    belong_system_info.service_object = ','.join(data.get('service_object'))
    belong_system_info.build_method = data.get('build_method')
    belong_system_info.system_type = ','.join(data.get('system_type'))
    belong_system_info.investment_total = data.get('investment_total')
    belong_system_info.funds_source = ','.join(data.get('funds_source'))
    belong_system_info.devops_expenses = data.get('devops_expenses')
    belong_system_info.person = data.get('person')
    belong_system_info.phone = data.get('phone')
    belong_system_info.department_id = data.get('belonging_department').get('dept_id')
    belong_system_info.notes = data.get('notes')
    belong_system_info.update_time = int(datetime.now().timestamp())
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/delete/belong_system', methods=['POST'])
@custom_jwt_required
def delete_belong_system():
    data = request.get_json()
    belong_system_info = BelongSystem.query.filter_by(id=data.get('id'),
                                                      department_id=data.get('department_id')).first()
    datasource_info = DatasourceInfo.query.filter_by(belonging_system_id=belong_system_info.id,
                                                     belonging_system_department_id=belong_system_info.department_id).first()
    if datasource_info:
        return jsonify({'code': 101, 'msg': "该信息系统已创建数据库连接，无法删除！"})
    db.session.delete(belong_system_info)
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/import/belong_system', methods=['POST'])
@custom_jwt_required
def import_belong_system():
    from backend.config import BASE_DIR
    import uuid
    file = request.files['file']
    user_id = request.form.get('userId')
    dept_id = request.form.get('deptId')
    if file:
        try:
            df = pd.read_excel(file)
            df.fillna('', inplace=True)
            data_list = df.to_dict(orient='records')
            success_list = []
            fail_list = []
            independent = False
            if len(data_list) > 0 and "*系统id" in data_list[0].keys():
                independent = True
            for data in data_list:
                system_name = str(data.get('*系统名称\n(最多50个字符)'))
                system_summary = str(data.get('*系统概述\n(最多200个字符)'))
                run_status = str(data.get('*运行状态\n(单选:在建、在用、停用)'))
                network_type = str(data.get('*网络类型\n(单选:互联网、电子政务外网、电子政务内网、行业专网、电子政务外网和互联网)'))
                construction_unit = str(data.get('*建设单位\n(最多50个字符)'))
                construction_company = str(data.get('*承建单位\n(最多50个字符)'))
                user_object = str(data.get('*使用对象\n(多选:企业、社会公众、部门内部,多个选项之间","隔开,逗号须英文格式的逗号)'))
                construction_method = str(data.get('*建设方式\n(单选:本级建设(或部署)政务信息系统、国家部委部署系统、其他)'))
                system_type = str(data.get('*系统类型\n(多选:基础设施、数据系统、业务系统、政务服务系统、其他,多个选项之间","隔开,逗号须英文格式的逗号)'))
                construction_cost = str(data.get('*建设费用(万元)\n(正数,最多2位小数)'))
                fund_source = str(data.get('*资金来源\n(多选:中央资金、省级资金、其他资金,多个选项之间","隔开,逗号须英文格式的逗号)'))
                annual_operation_cost = str(data.get('*本年度运维经费(万元)\n(正数,最多2位小数)'))
                fill_person_phone = str(data.get('*填报人手机号'))
                fill_person = str(data.get('*填报人\n(最多20个字符)'))
                notes = str(data.get('备注\n(最多200个字符)'))
                if len(system_name.strip()) == 0\
                        or len(system_summary.strip()) == 0\
                        or len(run_status.strip()) == 0\
                        or len(network_type.strip()) == 0\
                        or len(construction_unit.strip()) == 0\
                        or len(construction_company.strip()) == 0\
                        or len(user_object.strip()) == 0\
                        or len(construction_method.strip()) == 0\
                        or len(system_type.strip()) == 0\
                        or len(construction_cost.strip()) == 0\
                        or len(fund_source.strip()) == 0\
                        or len(annual_operation_cost.strip()) == 0\
                        or len(fill_person_phone.strip()) == 0\
                        or len(fill_person.strip()) == 0:
                    data['失败原因'] = '缺少必填字段'
                    fail_list.append(data)
                    continue
                if len(system_name) > 50:
                    data['失败原因'] = '系统名称字符大于50'
                    fail_list.append(data)
                    continue
                elif len(system_summary) > 200:
                    data['失败原因'] = '系统概述字符大于200'
                    fail_list.append(data)
                    continue
                elif run_status not in ('在建', '在用', '停用'):
                    data['失败原因'] = '运行状态字符不符合单选内容'
                    fail_list.append(data)
                    continue
                elif not all(s in ["互联网", "电子政务外网", "电子政务内网", "行业专网","电子政务外网和互联网"] for s in
                             [s.strip() for s in network_type.split(',')]):
                    data['失败原因'] = '网络类型字符中有不在多选内容的字符,请检查是否存在中文逗号'
                    fail_list.append(data)
                    continue
                elif len(str(construction_unit)) > 50:
                    data['失败原因'] = '建设单位字符大于50'
                    fail_list.append(data)
                    continue
                elif len(str(construction_company)) > 50:
                    data['失败原因'] = '承建单位字符大于50'
                    fail_list.append(data)
                    continue
                elif not all(s in ["企业", "社会公众", "部门内部"] for s in
                             [s.strip() for s in user_object.split(',')]):
                    data['失败原因'] = '使用对象字符中有不在多选内容的字符,请检查是否存在中文逗号'
                    fail_list.append(data)
                    continue
                elif construction_method not in ('本级建设(或部署)政务信息系统', '国家部委部署系统', '其他'):
                    data['失败原因'] = '建设方式字符不符合单选内容'
                    fail_list.append(data)
                    continue
                elif not all(s in ["基础设施", "数据系统", "业务系统", "政务服务系统", "其他"] for s in
                             [s.strip() for s in system_type.split(',')]):
                    data['失败原因'] = '系统类型字符中有不在多选内容的字符,请检查是否存在中文逗号'
                    fail_list.append(data)
                    continue
                elif str(construction_cost).find('.') != -1 and len(
                        str(construction_cost)[str(construction_cost).find('.') + 1:]) > 2:
                    data['失败原因'] = '建设费用大于2位小数'
                    fail_list.append(data)
                    continue
                elif not all(s in ["中央资金", "省级资金", "其他资金"] for s in
                             [s.strip() for s in fund_source.split(',')]):
                    data['失败原因'] = '资金来源字符中有不在多选内容的字符,请检查是否存在中文逗号'
                    fail_list.append(data)
                    continue
                elif str(annual_operation_cost).find('.') != -1 and len(
                        str(annual_operation_cost)[str(annual_operation_cost).find('.') + 1:]) > 2:
                    data['失败原因'] = '本年度运维经费运维经费大于2位小数'
                    fail_list.append(data)
                    continue
                elif len(fill_person) > 20:
                    data['失败原因'] = '填报人字符大于20'
                    fail_list.append(data)
                    continue
                elif len(str(notes)) > 200:
                    data['失败原因'] = '备注字符大于200'
                    fail_list.append(data)
                    continue
                if independent is True:
                    belonging_system_info = BelongSystem.query.filter_by(id=int(data.get('*系统id'))).first()
                    if not belonging_system_info:
                        belonging_system_info = BelongSystem(
                            id=int(data.get('*系统id')),
                            create_id=data.get('用户id'),
                            department_id=data.get('*所属部门id'),
                            system_name=system_name,
                            department=data.get('所属部门'),
                            belonging_department=data.get('所属处室'),
                            system_summary=system_summary,
                            run_status=run_status,
                            network=network_type,
                            build_unit=construction_unit,
                            construction_unit=construction_company,
                            service_object=user_object,
                            build_method=construction_method,
                            system_type=system_type,
                            investment_total=construction_cost,
                            funds_source=fund_source,
                            devops_expenses=annual_operation_cost,
                            person=fill_person,
                            phone=fill_person_phone,
                            notes=data.get('备注\n(最多200个字符)', ''),
                        )
                        db.session.add(belonging_system_info)
                    else:
                        belonging_system_info.system_name = system_name
                        belonging_system_info.create_id = data.get('用户id')
                        belonging_system_info.department_id=data.get('*所属部门id')
                        belonging_system_info.department = data.get('所属部门')
                        belonging_system_info.belonging_department = data.get('所属处室')
                        belonging_system_info.system_summary = system_summary
                        belonging_system_info.run_status = run_status
                        belonging_system_info.network = network_type
                        belonging_system_info.build_unit = construction_unit
                        belonging_system_info.construction_unit = construction_company
                        belonging_system_info.build_method = construction_method
                        belonging_system_info.system_type = system_type
                        belonging_system_info.service_object = user_object
                        belonging_system_info.investment_total = construction_cost
                        belonging_system_info.funds_source = fund_source
                        belonging_system_info.devops_expenses = annual_operation_cost
                        belonging_system_info.person = fill_person
                        belonging_system_info.phone = fill_person_phone
                        belonging_system_info.notes = notes
                    db.session.commit()
                else:
                    sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
                    if sys_dept.parent_id == 1:
                        department = sys_dept.dept_name
                        belonging_department = sys_dept.dept_name
                    else:
                        ancestors = sys_dept.ancestors.split(',')
                        ancestors = [i for i in ancestors if i != '']
                        department = SysDept.query.filter_by(parent_id=1).filter(SysDept.dept_id.in_(ancestors)).first().dept_name
                        belonging_department = sys_dept.dept_name
                    belonging_system = BelongSystem.query.filter_by(
                        system_name=system_name,
                        department=department,
                        belonging_department=belonging_department,
                        system_summary=system_summary,
                        run_status=run_status,
                        network=network_type,
                        build_unit=construction_unit,
                        construction_unit=construction_company,
                        service_object=user_object,
                        build_method=construction_method,
                        system_type=system_type,
                        investment_total=construction_cost,
                        funds_source=fund_source,
                        devops_expenses=annual_operation_cost,
                        person=fill_person,
                        phone=fill_person_phone,
                        notes=notes
                    ).first()
                    if not belonging_system:
                        belonging_system_info = BelongSystem(
                            id=random.randint(10 ** 15, 10 ** 16 - 1),
                            create_id=user_id,
                            department_id=dept_id,
                            system_name=system_name,
                            department=department,
                            belonging_department=belonging_department,
                            system_summary=system_summary,
                            run_status=run_status,
                            network=network_type,
                            build_unit=construction_unit,
                            construction_unit=construction_company,
                            service_object=user_object,
                            build_method=construction_method,
                            system_type=system_type,
                            investment_total=construction_cost,
                            funds_source=fund_source,
                            devops_expenses=annual_operation_cost,
                            person=fill_person,
                            phone=fill_person_phone,
                            notes=notes,
                        )
                        db.session.add(belonging_system_info)
                        db.session.commit()
                    else:
                        data['失败原因'] = '该系统已有一模一样系统信息'
                        fail_list.append(data)
                        continue
                success_list.append(data)
        except Exception as e:
            print(e)
            return jsonify({'code': 203, "msg": "数据格式有误,请检查后重试"})
        path = BASE_DIR + f'/template/system/{str(uuid.uuid4())}.xlsx'
        if len(fail_list) > 0:
            headers = list(fail_list[0].keys())
            json_data = pd.DataFrame(fail_list)
            json_data.columns = headers
            json_data.to_excel(path, index=False)
        data = {
            "success": len(success_list),
            "fail": len(fail_list),
            "file_path": path
        }
        return jsonify({'code': 200, "data": data})


@exploration_bp.route('/download/belong_system', methods=['POST'])
@custom_jwt_required
def download_belong_system():
    path = request.get_json().get('file_path')
    return send_file(path, as_attachment=True, download_name='导入失败原因.xlsx')


@exploration_bp.route('/export/belong_system', methods=['POST'])
@custom_jwt_required
def export_belong_system():
    from backend.config import BASE_DIR
    from backend.template.mapping import belong_system_mapping
    path = BASE_DIR + '/template/system.xlsx'
    data = request.get_json()
    user_id = data.get('userId')
    dept_id = data.get('deptId')
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=user_id).first()
    if sys_role.role_id in (1, 1855189077904728066, 1855189303667335169):
        ids_list = [sys_dept.dept_id for sys_dept in SysDept.query.all()]
    elif sys_role.role_id == 1855188956748062721:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id != 1:
            ancestors = sys_dept.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            sys_dept = SysDept.query.filter(and_(
                SysDept.dept_id.in_(ancestors),
                SysDept.parent_id == 1
            )).first()
        _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
        ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
        ids_list.append(sys_dept.dept_id)
    else:
        ids_list = [dept_id]
    query = BelongSystem.query.filter(
        and_(
            BelongSystem.department_id.in_(ids_list),
        )
    )
    belong_systems = query.all()
    json_list = []
    desired_order = [
        '*系统id',
        '*系统名称\n(最多50个字符)',
        '*所属部门id',
        '所属部门',
        '所属处室',
        '*系统概述\n(最多200个字符)',
        '*运行状态\n(单选:在建、在用、停用)',
        '*网络类型\n(单选:互联网、电子政务外网、电子政务内网、行业专网、电子政务外网和互联网)',
        '*建设单位\n(最多50个字符)',
        '*承建单位\n(最多50个字符)',
        '*使用对象\n(多选:企业、社会公众、部门内部,多个选项之间","隔开,逗号须英文格式的逗号)',
        '*建设方式\n(单选:本级建设(或部署)政务信息系统、国家部委部署系统、其他)',
        '*系统类型\n(多选:基础设施、数据系统、业务系统、政务服务系统、其他,多个选项之间","隔开,逗号须英文格式的逗号)',
        '*建设费用(万元)\n(正数,最多2位小数)',
        '*资金来源\n(多选:中央资金、省级资金、其他资金,多个选项之间","隔开,逗号须英文格式的逗号)',
        '*本年度运维经费(万元)\n(正数,最多2位小数)',
        '*填报人\n(最多20个字符)',
        '*填报人手机号',
        '备注\n(最多200个字符)',
        '用户id'
    ]
    for belong_system in belong_systems:
        belong_system = belong_system.__dict__
        translated_data = {}
        for key, value in belong_system.items():
            if key in ('_sa_instance_state', 'create_time', 'update_time'):
                continue
            if key in ('id','department_id'):
                value = str(value)
            translated_key = belong_system_mapping.get(key, key)
            translated_data[translated_key] = value
        ordered_dict = {key: translated_data[key] for key in desired_order if key in translated_data}
        json_list.append(ordered_dict)
    headers = list(json_list[0].keys())
    json_data = pd.DataFrame(json_list)
    json_data.columns = headers
    json_data.to_excel(path, index=False)
    return send_file(path, as_attachment=True, download_name='系统清单.xlsx')


@exploration_bp.route('/create/datasource', methods=['POST'])
@custom_jwt_required
def create_datasource():
    # cur_name = get_jwt_identity()
    data = request.get_json()
    database_address = data.get('database_address') + ':' + data.get('port')
    datasource_info = DatasourceInfo(
        datasource_name=data.get('datasource_name'),
        database_type=data.get('database_type'),
        belonging_system_id=data.get('belonging_system_id'),
        belonging_system_department_id=data.get('belonging_system_department_id'),
        # user_admin_id=user_admin_id,
        database_name=data.get('database_name'),
        database_address=database_address,
        database_username=data.get('database_username'),
        schema_name=data.get('schema_name'),
        database_password=encrypt_password(data.get('database_password')),
        create_id=data.get('userId'),
        status=data.get('status'),
        table_name=data.get('table_name',None)
    )
    db.session.add(datasource_info)
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/query/datasource', methods=['GET'])
@custom_jwt_required
def query_datasource():
    create_id = request.args.get('userId')
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=create_id).first()
    create_id = [create_id]
    if sys_role.role_id == 1:
        sys_users = SysUser.query.all()
        create_id = [_sys_user.user_id for _sys_user in sys_users]
    datasource_infos = DatasourceInfo.query.filter(DatasourceInfo.create_id.in_(create_id)).all()
    datasource_info_list = [datasource_info.__dict__ for datasource_info in datasource_infos]
    datasource_info_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                            datasource_info_list]
    return jsonify({'code': 200, 'data': datasource_info_list})


@exploration_bp.route('/query/filter/datasource', methods=['POST'])
@custom_jwt_required
def query_filter_datasource():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    datasource_name = data.get('datasource_name', None)
    belonging_system_id = data.get('belonging_system_id', None)
    belonging_system_department_id = data.get('belonging_system_department_id', None)
    belonging_department = data.get('belonging_department', None)
    dept_id = data.get('deptId')
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=data.get('userId')).first()
    if sys_role.role_id in (1, 1855189077904728066, 1855189303667335169):
        ids_list = [sys_dept.dept_id for sys_dept in SysDept.query.all()]
    elif sys_role.role_id == 1855188956748062721:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id != 1:
            ancestors = sys_dept.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            sys_dept = SysDept.query.filter(and_(
                SysDept.dept_id.in_(ancestors),
                SysDept.parent_id == 1
            )).first()
        _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
        ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
        ids_list.append(sys_dept.dept_id)
    else:
        ids_list = [dept_id]
    if belonging_department:
        sys_dept = SysDept.query.filter_by(dept_id=data.get('belonging_department')).first()
        if sys_dept.parent_id == 1:
            _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
            id_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
            id_list.append(sys_dept.dept_id)
        else:
            id_list = [sys_dept.dept_id]
        ids_list = list(set(ids_list) & set(id_list))

    belongsystem_ids = [i.id for i in BelongSystem.query.filter(
        and_(
            BelongSystem.department_id.in_(ids_list),
        )
    ).all()]
    query = DatasourceInfo.query.filter(DatasourceInfo.belonging_system_id.in_(belongsystem_ids))
    if datasource_name:
        query = DatasourceInfo.query.filter(DatasourceInfo.belonging_system_id.in_(belongsystem_ids)).filter(
            DatasourceInfo.datasource_name.like(f"%{datasource_name}%"))
    if belonging_system_id and belonging_system_department_id:
        query = (DatasourceInfo.query.filter(DatasourceInfo.belonging_system_id.in_(belongsystem_ids))
                 .join(BelongSystem, (BelongSystem.id == DatasourceInfo.belonging_system_id) & (
                BelongSystem.department_id == DatasourceInfo.belonging_system_department_id))
                 .filter_by(id=belonging_system_id, department_id=belonging_system_department_id))

    if datasource_name and belonging_system_id and belonging_system_department_id:
        query = (DatasourceInfo.query.filter(DatasourceInfo.belonging_system_id.in_(belongsystem_ids)).filter(
            DatasourceInfo.datasource_name.like(f"%{datasource_name}%"))
                 .join(BelongSystem, (BelongSystem.id == DatasourceInfo.belonging_system_id) & (
                BelongSystem.department_id == DatasourceInfo.belonging_system_department_id))
                 .filter_by(id=belonging_system_id, department_id=belonging_system_department_id))
    query = query.order_by(DatasourceInfo.create_time.desc())
    count = query.count()
    datasource_infos = query.paginate(page=page, per_page=per_page).items
    for datasource_info in datasource_infos:
        datasource_dict = datasource_info.__dict__
        belonging_system_info = BelongSystem.query.filter_by(id=datasource_dict.get('belonging_system_id')).first()
        sys_user = SysUser.query.filter_by(user_id=datasource_dict.get('create_id')).first()
        database_address = datasource_dict['database_address'].split(':')
        datasource_dict['database_address'] = database_address[0]
        datasource_dict['port'] = database_address[1]
        datasource_dict['system_name'] = belonging_system_info.system_name
        datasource_dict['department'] = belonging_system_info.department
        datasource_dict['belonging_department'] = belonging_system_info.belonging_department
        datasource_dict['create_by'] = sys_user.nick_name
    datasource_info_list = [datasource_info.__dict__ for datasource_info in datasource_infos]
    datasource_info_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                            datasource_info_list]
    data = {
        'data': datasource_info_list,
        'count': count,
        'page': page,
        'per_page': per_page
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/update/datasource', methods=['POST'])
@custom_jwt_required
def update_datasource():
    data = request.get_json()
    datasource_info = DatasourceInfo.query.filter_by(id=data.get('id')).first()
    datasource_info.datasource_name = data.get('datasource_name')
    datasource_info.database_type = data.get('database_type')
    datasource_info.department = data.get('department')
    datasource_info.belonging_system = data.get('belonging_system')
    datasource_info.database_name = data.get('database_name')
    datasource_info.database_address = data.get('database_address') + ':' + data.get('port')
    datasource_info.database_username = data.get('database_username')
    datasource_info.database_password = encrypt_password(data.get('database_password'))
    datasource_info.belonging_system_id = data.get('belonging_system_id')
    datasource_info.schema_name = data.get('schema_name')
    datasource_info.belonging_system_department_id = data.get('belonging_system_department_id')
    datasource_info.status = data.get('status')
    datasource_info.table_name = data.get('table_name')
    datasource_info.update_time = int(datetime.now().timestamp())
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/delete/datasource', methods=['POST'])
@custom_jwt_required
def delete_datasource():
    data = request.get_json()
    datasource_info = DatasourceInfo.query.filter_by(id=data.get('id')).first()
    schedule = ScheduleInfo.query.filter_by(datasource_id=datasource_info.id).first()
    if schedule:
        return jsonify({'code': 101, 'msg': "该数据库连接已有探查任务，无法删除！"})
    db.session.delete(datasource_info)
    db.session.commit()
    return jsonify({'code': 200,'msg':'删除成功'})



@exploration_bp.route('/test_connect', methods=['POST'])
@custom_jwt_required
def test_connect():
    # import cx_Oracle
    # cx_Oracle.init_oracle_client(lib_dir="/root/instantclient_12_2")
    try:
        data = request.get_json()
        database_type = data.get('database_type')
        database_name = data.get('database_name')
        database_address = data.get('database_address')
        prot = data.get('port')
        username = data.get('database_username')
        password = urllib.parse.quote_plus(data.get('database_password'))
        if database_type == 'dmdb':
            password = data.get('database_password')
        if database_type == 'sqlite':
            db_url = f'sqlite:///{database_address}'
        if database_type == 'mysql':
            db_url = f"mysql+pymysql://{username}:{password}@{database_address}:{prot}/{database_name}"
        if database_type == 'postgresql':
            db_url = f"postgresql://{username}:{password}@{database_address}:{prot}/{database_name}"
        if database_type == 'oracle':
            db_url = f'oracle+cx_oracle://{username}:{password}@{database_address}:{prot}/?service_name={database_name}'
        if database_type == 'sql_server':
            db_url = f'mssql+pyodbc://{username}:{password}@{database_address}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
        if database_type == 'dmdb':
            conn = dmPython.connect(user=username, password=password, server=database_address, port=prot)
            # conn.connect()
            return jsonify({'code': 200})
        engine = create_engine(db_url)
        engine.connect()
        return jsonify({'code': 200})
    except Exception as e:
        logging.info(str(e))
        print(e)
        return jsonify({'code': 203, 'msg': '连接失败，请检查数据库连接信息是否错误'})


@exploration_bp.route('/schedule/add', methods=['POST'])
@custom_jwt_required
def schedule_add():
    data = request.get_json()
    minute = data.get('minute')
    hour = data.get('hour')
    day = data.get('day')
    week = data.get('week')
    schedule_info = ScheduleInfo.query.filter_by(datasource_id=data.get('datasource_id')).first()
    if schedule_info:
        return jsonify({'code':203,'msg':'该数据库连接已有探查任务，不能重复创建!'})
    schedule_info = ScheduleInfo(
        datasource_id=data.get('datasource_id'),
        schedule_name=data.get('schedule_name'),
        minute=minute,
        hour=hour,
        day=day,
        week=week,
        method=data.get('method'),
        name=str(uuid.uuid4()),
        create_id=data.get('userId'),
        department_id=data.get('deptId')
    )
    db.session.add(schedule_info)
    db.session.commit()
    system_info = (BelongSystem.query
                   .join(DatasourceInfo, (BelongSystem.id == DatasourceInfo.belonging_system_id) & (
            BelongSystem.department_id == DatasourceInfo.belonging_system_department_id))
                   .filter_by(id=data.get('datasource_id')).first())
    data['schedule_name'] = schedule_info.schedule_name
    data['schedule_id'] = schedule_info.id
    data['create_id'] = schedule_info.create_id
    data['department_id'] = schedule_info.department_id
    data['up_cycle'] = '循环定时任务'
    data['system_id'] = system_info.id
    data['schedule_type'] = 'time'
    r.publish('scheduler', json.dumps(data))
    return jsonify({'code': 200})


@exploration_bp.route('/schedule/immediately', methods=['POST'])
@custom_jwt_required
def schedule_immediately():
    data = request.get_json()
    scheduler_ids = data.get('schedule_ids')
    for scheduler_id in scheduler_ids:
        schedule_info = ScheduleInfo.query.filter_by(id=scheduler_id).first()
        schedule_execute_total = ScheduleExecute.query.filter_by(schedule_status='执行中').count()
        print(schedule_execute_total)
        print(config.get('thread'))
        if schedule_execute_total >= config.get('thread'):
            return jsonify({'code': 203, 'msg': '超过系统任务最大执行数，请稍后再试!'})
        data['datasource_id'] = schedule_info.datasource_id
        data['schedule_id'] = scheduler_id
        data['schedule_name'] = schedule_info.schedule_name
        data['schedule_type'] = "immediately"
        data_copy = copy.deepcopy(data)
        r.publish('scheduler', json.dumps(data_copy))
    # json_object = json.dumps({"code": 200})
    # yield f"event:message\ndata:" + json_object + "\n\n"
    return jsonify({'code': 200})


@exploration_bp.route('/schedule/update', methods=['POST'])
@custom_jwt_required
def schedule_update():
    data = request.get_json()
    count = ScheduleInfo.query.filter_by(datasource_id=data.get('datasource_id')).count()
    schedule_info = ScheduleInfo.query.filter_by(id=data.get('id')).first()
    if schedule_info.datasource_id != data.get('datasource_id') and count == 1:
        return jsonify({'code': 203, 'msg': '该数据库连接已有探查任务，不能重复创建!'})
    schedule_info.schedule_name = data.get('schedule_name')
    schedule_info.datasource_id = data.get('datasource_id')
    schedule_info.method = data.get('method')
    schedule_info.day = data.get('day')
    schedule_info.minute = data.get('minute')
    schedule_info.hour = data.get('hour')
    schedule_info.week = data.get('week')
    schedule_info.update_time = int(datetime.now().timestamp())
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/schedule/delete', methods=['POST'])
@custom_jwt_required
def schedule_delete():
    data = request.get_json()
    schedule_infos = ScheduleInfo.query.filter_by(id=data.get('id')).first()
    data['schedule_type'] = 'delete'
    r.publish('scheduler', json.dumps(data))
    db.session.delete(schedule_infos)
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/schedule/query', methods=['GET'])
@custom_jwt_required
def schedule_query():
    schedule_execute = ScheduleExecute.query.all()
    schedule_execute_infos_list = []
    for schedule_execute_info in schedule_execute:
        schedule_execute_dict = schedule_execute_info.__dict__
        datasource_info = DatasourceInfo.query.filter_by(id=schedule_execute_dict.get('datasource_id')).first()
        schedule_execute_dict['datasource_name'] = datasource_info.datasource_name
        schedule_execute_infos_list.append(schedule_execute_dict)
    schedule_execute_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                                   schedule_execute_infos_list]
    return jsonify({'code': 200, 'data': schedule_execute_infos_list})


@exploration_bp.route('/schedule/filter/query', methods=['POST'])
@custom_jwt_required
def schedule_filter_query():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    schedule_id = data.get('schedule_id', None)
    schedule_name = data.get('schedule_name', None)
    datasource_name = data.get('datasource_name', None)
    mode = data.get('mode', None)
    status = data.get('status', None)
    dept_id = data.get('deptId')
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=data.get('userId')).first()
    if sys_role.role_id in (1, 1855189077904728066, 1855189303667335169):
        ids_list = [sys_dept.dept_id for sys_dept in SysDept.query.all()]
    elif sys_role.role_id == 1855188956748062721:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id != 1:
            ancestors = sys_dept.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            sys_dept = SysDept.query.filter(and_(
                SysDept.dept_id.in_(ancestors),
                SysDept.parent_id == 1
            )).first()
        _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
        ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
        ids_list.append(sys_dept.dept_id)
    else:
        ids_list = [dept_id]
    belongsystem_ids = [i.id for i in BelongSystem.query.filter(
        and_(
            BelongSystem.department_id.in_(ids_list),
        )
    ).all()]
    query = ScheduleExecute.query.join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if mode:
        query = ScheduleExecute.query.join(DatasourceInfo).filter_by(status=mode).join(BelongSystem,
                                                                BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.id.in_(belongsystem_ids))

    if schedule_name:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))

    if mode and schedule_name:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).join(
            DatasourceInfo).filter_by(status=mode).join(BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.id.in_(belongsystem_ids))

    if datasource_name:
        query = ScheduleExecute.query.filter_by(
            datasource_id=datasource_name).join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if status:
        query = ScheduleExecute.query.filter_by(schedule_status=status).join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_id:
        query = ScheduleExecute.query.filter_by(schedule_id=schedule_id).join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))

    if schedule_id and schedule_name:
        query = ScheduleExecute.query.filter_by(schedule_id=schedule_id).filter(
            ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_id and datasource_name:
        query = ScheduleExecute.query.filter_by(schedule_id=schedule_id).filter_by(
            datasource_id=datasource_name).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_id and status:
        query = ScheduleExecute.query.filter_by(schedule_id=schedule_id, schedule_status=status).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name and datasource_name:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            datasource_id=datasource_name).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name and status:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            schedule_status=status).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name and status and mode:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            schedule_status=status).join(
            DatasourceInfo).filter_by(status=mode).join(BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.id.in_(belongsystem_ids))

    if datasource_name and status:
        query = ScheduleExecute.query.filter_by(schedule_status=status).filter_by(
            datasource_id=datasource_name).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))

    if schedule_id and schedule_name and datasource_name:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            schedule_id=schedule_id).filter_by(datasource_id=datasource_name).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_id and schedule_name and status:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            schedule_status=status,
            schedule_id=schedule_id).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_id and datasource_name and status:
        query = ScheduleExecute.query.filter_by(schedule_status=status,
                                                schedule_id=schedule_id).filter_by(datasource_id=datasource_name).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name and datasource_name and status:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            datasource_id=datasource_name).filter_by(schedule_status=status).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))

    if schedule_id and schedule_name and datasource_name and status:
        query = ScheduleExecute.query.filter(ScheduleExecute.schedule_name.like(f"%{schedule_name}%")).filter_by(
            schedule_status=status,
            schedule_id=schedule_id).filter_by(datasource_id=datasource_name).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))

    count = query.count()
    schedule_execute = query.order_by(ScheduleExecute.create_time.desc()).paginate(page=page, per_page=per_page).items
    schedule_execute_infos_list = []
    for schedule_execute_info in schedule_execute:
        schedule_execute_dict = schedule_execute_info.__dict__
        datasource_info = DatasourceInfo.query.filter_by(id=schedule_execute_dict.get('datasource_id')).first()
        schedule_info = ScheduleInfo.query.filter_by(id=schedule_execute_dict.get('schedule_id')).first()
        schedule_execute_dict['datasource_name'] = datasource_info.datasource_name
        schedule_execute_dict['mode'] = '系统探查' if datasource_info.status == '1' else '结果表探查'
        schedule_execute_dict['schedule_name'] = schedule_info.schedule_name
        schedule_execute_infos_list.append(schedule_execute_dict)
    schedule_execute_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                                   schedule_execute_infos_list]
    data = {
        'data': schedule_execute_infos_list,
        'count': count,
        'page': page,
        'per_page': per_page
    }
    return jsonify({'code': 200, 'data': data})

@exploration_bp.route('/schedule/filter/id/query', methods=['POST'])
@custom_jwt_required
def schedule_filter_query_get():
    data = request.get_json()
    schedule_id = data.get('schedule_id', None)
    schedule_execute_info = ScheduleExecute.query.filter_by(schedule_id=schedule_id).filter_by(schedule_status="成功").join(DatasourceInfo).order_by(ScheduleExecute.create_time.desc()).first()
    schedule_execute_infos_list = []
    if schedule_execute_info is not None:
        schedule_execute_dict = schedule_execute_info.__dict__
        datasource_info = DatasourceInfo.query.filter_by(id=schedule_execute_dict.get('datasource_id')).first()
        schedule_execute_dict['datasource_name'] = datasource_info.datasource_name
        schedule_execute_dict['mode'] = '系统探查' if datasource_info.status == '1' else '结果表探查'
        schedule_execute_infos_list.append(schedule_execute_dict)
        schedule_execute_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                                       schedule_execute_infos_list]
    data = {
        'data': schedule_execute_infos_list,
    }
    return jsonify({'code': 200, 'data': data})



@exploration_bp.route('/schedule/shutdown', methods=['POST'])
@custom_jwt_required
def schedule_shutdown():
    data = request.get_json()
    schedule_infos = ScheduleInfo.query.filter_by(id=data.get('id')).first()
    data['schedule_type'] = 'delete'
    r.publish('scheduler', json.dumps(data))
    schedule_infos.is_start = False
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/schedule/start', methods=['POST'])
@custom_jwt_required
def schedule_start():
    data = request.get_json()
    schedule_info = ScheduleInfo.query.filter_by(id=data.get('id')).first()
    hour = schedule_info.hour
    minute = schedule_info.minute
    day = schedule_info.day
    week = schedule_info.week
    data = {
        'datasource_id': schedule_info.datasource_id,
        'schedule_id': schedule_info.id,
        'schedule_name': schedule_info.schedule_name,
        'schedule_type': 'time'
    }
    r.publish('scheduler', json.dumps(data))
    # try:
    #     if schedule_info.method == 'day':
    #         scheduler.add_job(func=_data_exploration, trigger='cron', id=str(schedule_info.id),
    #                           name=schedule_info.name, args=[data],
    #                           hour=hour,
    #                           minute=minute)
    #     if schedule_info.method == 'week':
    #         scheduler.add_job(func=_data_exploration, trigger='cron', id=str(schedule_info.id),
    #                           name=schedule_info.name, args=[data],
    #                           hour=hour,
    #                           minute=minute, day_of_week=week)
    #     if schedule_info.method == 'month':
    #         scheduler.add_job(func=_data_exploration, trigger='cron', id=str(schedule_info.id),
    #                           name=schedule_info.name, args=[data],
    #                           hour=hour,
    #                           minute=minute, day=day)
    schedule_info.is_start = True
    # except  Exception as e:
    #     name = scheduler.get_job(str(schedule_info.id)).name
    #     return jsonify({'code': 203,'msg':str(e),'name':name})
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/exploration/query')
@custom_jwt_required
def exploration_query():
    department_id = request.args.get('deptId')
    schedule_infos = ScheduleInfo.query.join(DatasourceInfo).join(BelongSystem).filter_by(
        department_id=department_id).all()
    schedule_infos_list = []
    for schedule_info in schedule_infos:
        schedule_info_dict = schedule_info.__dict__
        datasource_info = DatasourceInfo.query.filter_by(id=schedule_info_dict.get('datasource_id')).first()
        schedule_info_dict['datasource_name'] = datasource_info.datasource_name
        schedule_infos_list.append(schedule_info_dict)
    schedule_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                           schedule_infos_list]
    return jsonify({'code': 200, 'data': schedule_infos_list})


@exploration_bp.route('/exploration/filter/query', methods=['POST'])
@custom_jwt_required
def exploration_filter_query():
    data = request.get_json()
    page = data.get('page')
    per_page = data.get('per_page')
    schedule_name = data.get('schedule_name', None)
    datasource_name = data.get('datasource_name', None)
    mode = data.get('mode', None)
    belonging_department = data.get('belonging_department', None)
    dept_id = data.get('deptId')
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=data.get('userId')).first()
    if sys_role.role_id in (1, 1855189077904728066, 1855189303667335169):
        ids_list = [sys_dept.dept_id for sys_dept in SysDept.query.all()]
    elif sys_role.role_id == 1855188956748062721:
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id != 1:
            ancestors = sys_dept.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            sys_dept = SysDept.query.filter(and_(
                SysDept.dept_id.in_(ancestors),
                SysDept.parent_id == 1
            )).first()
        _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
        ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
        ids_list.append(sys_dept.dept_id)
    else:
        ids_list = [dept_id]
    if belonging_department:
        sys_dept = SysDept.query.filter_by(dept_id=data.get('belonging_department')).first()
        if sys_dept.parent_id == 1:
            _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{sys_dept.dept_id}")).all()
            id_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
            id_list.append(sys_dept.dept_id)
        else:
            id_list = [sys_dept.dept_id]
        ids_list = list(set(ids_list) & set(id_list))
    belongsystem_ids = [i.id for i in BelongSystem.query.filter(
        and_(
            BelongSystem.department_id.in_(ids_list),
        )
    ).all()]
    query = ScheduleInfo.query.join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name:
        query = ScheduleInfo.query.filter(ScheduleInfo.schedule_name.like(f"%{schedule_name}%")).join(
            DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if datasource_name:
        query = ScheduleInfo.query.filter_by(datasource_id=datasource_name).join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if mode:
        query = ScheduleInfo.query.join(DatasourceInfo).filter_by(status=mode).join(BelongSystem,
                                                             BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.id.in_(belongsystem_ids))

    if schedule_name and datasource_name:
        query = ScheduleInfo.query.filter(ScheduleInfo.schedule_name.like(f"%{schedule_name}%")).filter_by(
            datasource_id=datasource_name).join(DatasourceInfo).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name and mode:
        query = ScheduleInfo.query.filter(ScheduleInfo.schedule_name.like(f"%{schedule_name}%")).join(
            DatasourceInfo).filter_by(status=mode).join(BelongSystem, BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.id.in_(belongsystem_ids))
    if datasource_name and mode:
        query = ScheduleInfo.query.filter_by(datasource_id=datasource_name).join(DatasourceInfo).filter_by(status=mode).join(BelongSystem,BelongSystem.id == DatasourceInfo.belonging_system_id).filter(BelongSystem.id.in_(belongsystem_ids))
    if schedule_name and datasource_name and mode:
        query = ScheduleInfo.query.filter(ScheduleInfo.schedule_name.like(f"%{schedule_name}%")).filter_by(
            datasource_id=datasource_name).join(DatasourceInfo).filter_by(status=mode).join(BelongSystem,
                                                                     BelongSystem.id == DatasourceInfo.belonging_system_id).filter(
            BelongSystem.id.in_(belongsystem_ids))
    count = query.count()
    schedule_infos = query.all()
    schedule_infos_list = []
    for schedule_info in schedule_infos:
        schedule_info_dict = schedule_info.__dict__
        datasource_info = DatasourceInfo.query.filter_by(id=schedule_info_dict.get('datasource_id')).first()
        sys_user = SysUser.query.filter_by(user_id=datasource_info.create_id).first()
        schedule_execute = ScheduleExecute.query.filter_by(schedule_id=schedule_info.id).order_by(
            ScheduleExecute.schedule_time.desc()).first()
        if schedule_execute:
            execute_time = schedule_execute.schedule_time
            execute_status = schedule_execute.schedule_status
        else:
            execute_time = ''
            execute_status = ''
        if schedule_info.method == 'day':
            methods = '每天'
        elif schedule_info.method == 'week':
            methods = '每周'
        else:
            methods = '每月'
        schedule_info_dict['datasource_name'] = datasource_info.datasource_name
        schedule_info_dict['execute_time'] = execute_time
        schedule_info_dict['methods'] = methods
        schedule_info_dict['create_by'] = sys_user.nick_name
        schedule_info_dict['mode'] = '系统探查' if datasource_info.status =='1' else '结果表探查'
        schedule_info_dict['execute_status'] = False if execute_status=='执行中' else True
        schedule_infos_list.append(schedule_info_dict)
    schedule_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in schedule_infos_list]
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    schedule_infos_list = schedule_infos_list[start_index:end_index]
    data = {
        'data': schedule_infos_list,
        'count': count,
        'page': page,
        'per_page': per_page
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/metadata/table/query', methods=['GET'])
@custom_jwt_required
def metadata_table_query():
    table_infos = TableInfo.query.all()
    table_infos_list = []
    field_count_total = 0
    for table_info in table_infos:
        table_info_dict = table_info.__dict__
        field_count = FieldInfo.query.filter_by(table_info_id=table_info_dict.get('id')).count()
        field_count_total += field_count
        table_info_dict['field_count'] = field_count
        table_infos_list.append(table_info_dict)
    table_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                        table_infos_list]
    return jsonify({'code': 200, 'data': table_infos_list})


@exploration_bp.route('/metadata/table/filter/query', methods=['POST'])
@custom_jwt_required
def metadata_table_filter_query():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    schedule_id = data.get('schedule_id')
    table_name = data.get('schedule_name', None)
    contrast_status = data.get('status', None)
    if contrast_status == '新增':
        change_status = 0
    elif contrast_status == '变更':
        change_status = 1
    else:
        change_status = 2
    sort_key = data.get('sort_key', None)
    order = data.get('desc', 'asc')
    query = TableHistoryTemplateInfo.query.filter_by(schedule_execute_id=schedule_id).order_by(TableHistoryTemplateInfo.change_status.asc())
    if table_name:
        query = TableHistoryTemplateInfo.query.filter_by(schedule_execute_id=schedule_id).filter(
            TableHistoryTemplateInfo.table_name.like(f"%{table_name}%")).order_by(TableHistoryTemplateInfo.change_status.asc())
    if contrast_status:
        query = TableHistoryTemplateInfo.query.filter_by(schedule_execute_id=schedule_id).filter_by(
            change_status=change_status).order_by(TableHistoryTemplateInfo.change_status.asc())
    if table_name and contrast_status:
        query = TableHistoryTemplateInfo.query.filter_by(schedule_execute_id=schedule_id).filter(
            TableHistoryTemplateInfo.table_name.like(f"%{table_name}%")).filter_by(change_status=change_status).order_by(TableHistoryTemplateInfo.change_status.asc())
    table_infos = query.order_by(TableHistoryTemplateInfo.data_total_change.desc()).all()
    table_infos_list = []
    table_id = [table_info.id for table_info in table_infos]
    field_count_total = FieldHistoryInfo.query.join(TableHistoryInfo).filter_by(schedule_execute_id=schedule_id).count()
    add_table = DatabaseChangeLog.query.filter_by(change_type='table', change_status='add').filter(
        DatabaseChangeLog.table_info_id.in_(table_id)).count()
    update_table = DatabaseChangeLog.query.filter_by(change_type='table', change_status='update').filter(
        DatabaseChangeLog.table_info_id.in_(table_id)).count()
    add_field_count = DatabaseChangeLog.query.filter_by(change_type='field', change_status='add').filter(
        DatabaseChangeLog.table_info_id.in_(table_id)).count()
    update_field = DatabaseChangeLog.query.filter_by(change_type='field', change_status='update').filter(
        DatabaseChangeLog.table_info_id.in_(table_id)).count()
    delete_table_count = DatabaseChangeLog.query.filter_by(change_type='table', change_status='delete').filter(
        DatabaseChangeLog.table_info_id.in_(table_id)).count()
    delete_field_count = DatabaseChangeLog.query.filter_by(change_type='field', change_status='delete').filter(
        DatabaseChangeLog.table_info_id.in_(table_id)).count()
    for table_info in table_infos:
        table_info_dict = table_info.__dict__
        # print(table_change.change_status)
        if table_info.change_status == 0:
            change_status = '新增'
        elif table_info.change_status == 1:
            change_status = '变更'
        else:
            change_status = '一致'
        table_info_dict['change_status'] = change_status
        table_infos_list.append(table_info_dict)
    table_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                        table_infos_list]
    if sort_key:
        if order == 'asc':
            table_infos_list = sorted(table_infos_list, key=lambda x: x[sort_key])
        else:
            table_infos_list = sorted(table_infos_list, key=lambda x: x[sort_key], reverse=True)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    table_infos_list = table_infos_list[start_index:end_index]
    data = {
        'data': table_infos_list,
        'table_total': TableHistoryInfo.query.filter_by(schedule_execute_id=schedule_id).count(),
        'add_table': add_table,
        'update_table': update_table,
        'field_count_total': field_count_total,
        'add_field_count': add_field_count,
        'update_field': update_field,
        'delete_table_count': delete_table_count,
        'delete_field_count': delete_field_count
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/metadata/field/filter/query', methods=['POST'])
@custom_jwt_required
def metadata_field_filter_query():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    schedule_id = data.get('schedule_id')
    table_info_id = data.get('table_info_id')
    field_name = data.get('field_name', None)
    contrast_status = data.get('contrast_status', None)
    query = FieldHistoryInfo.query.filter_by(table_info_id=table_info_id)
    if field_name:
        query = FieldHistoryInfo.query.filter_by(table_info_id=table_info_id, name=field_name)
    if contrast_status:
        query = FieldHistoryInfo.query.filter_by(table_info_id=table_info_id).join(DatabaseChangeLog).filter_by(
            change_status=contrast_status)

    if field_name and contrast_status:
        query = FieldHistoryInfo.query.filter_by(table_info_id=table_info_id, name=field_name).join(
            DatabaseChangeLog).filter_by(change_status=contrast_status)

    field_infos = query.all()
    field_count_total = FieldHistoryInfo.query.filter_by(table_info_id=table_info_id).count()
    add_field_count = DatabaseChangeLog.query.filter_by(table_info_id=table_info_id, change_status='add',
                                                        change_type='field').count()
    field_infos_list = []
    for field_info in field_infos:
        field_change_info = DatabaseChangeLog.query.filter_by(field_info_id=field_info.id).first()
        field_info_dict = field_info.__dict__
        if field_change_info.change_status == 'add':
            change_status = '新增'
        elif field_change_info.change_status == 'update':
            change_status = '变更'
        else:
            change_status = '一致'
        field_info_dict['change_status'] = change_status
        field_infos_list.append(field_info_dict)
    field_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                        field_infos_list]
    status_order = {'新增': 1, '变更': 2, '一致': 3}
    field_infos_list = sorted(field_infos_list, key=lambda x: status_order[x['change_status']])
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    field_infos_list = field_infos_list[start_index:end_index]
    data = {
        'data': field_infos_list,
        'field_count_total': field_count_total,
        'add_field_count': add_field_count
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/upload/resources', methods=['POST'])
@custom_jwt_required
def upload_resources():
    if 'file' not in request.files:
        return 'No file part', 400
    files = request.files.getlist('file')
    dept_id = request.form['deptId']
    user_id = request.form['userId']
    for file in files:
        if file.filename == '':
            return 'No selected file', 400
        if file:
            filename = file.filename
            save_path = config.get('excel_file') + '/' + filename
            file.save(save_path)
            data_resources = DataResources(
                dept_id=dept_id,
                file_path=save_path,
                file_name=filename,
                create_id=user_id,
                update_id=user_id
            )
            db.session.add(data_resources)
            db.session.commit()
    return jsonify({"code": 200})


@exploration_bp.route('/query/resources', methods=['POST'])
@custom_jwt_required
def query_resources():
    data = request.get_json()
    dept_id = data.get('deptId')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    if dept_id != '':
        query = DataResources.query.filter_by(dept_id=dept_id)
    else:
        query = DataResources.query
    total = query.count()
    data_resources = query.paginate(page=page, per_page=per_page).items
    data_resources_list = []
    for data_resource in data_resources:
        data_resource = data_resource.__dict__
        create_user = SysUser.query.filter_by(user_id=data_resource.get('create_id')).first()
        update_user = SysUser.query.filter_by(user_id=data_resource.get('update_id')).first()
        dept = SysDept.query.filter_by(dept_id=data_resource.get('dept_id')).first()
        data_resource['create_by'] = create_user.nick_name
        data_resource['update_by'] = update_user.nick_name
        data_resource['dept_name'] = dept.dept_name
        data_resources_list.append(data_resource)
    data_resources_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                           data_resources_list]
    data = {
        "page": page,
        "per_page": per_page,
        "data": data_resources_list,
        "total":total
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/query/auth/resources', methods=['POST'])
@custom_jwt_required
def query_auth_resources():
    data = request.get_json()
    user_id = data.get('userId')
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    query = DataResources.query.join(DataResourcesAuth,DataResources.id==DataResourcesAuth.data_resources_id).filter_by(user_id=user_id)
    total = query.count()
    data_resources = query.paginate(page=page, per_page=per_page).items
    data_resources_list = []
    for data_resource in data_resources:
        data_resource = data_resource.__dict__
        data_resources_list.append(data_resource)
    data_resources_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                           data_resources_list]
    data = {
        "page": page,
        "per_page": per_page,
        "data": data_resources_list,
        "total":total
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/query/resources/result',methods=['POST'])
@custom_jwt_required
def query_resources_result():
    data = request.get_json()
    user_id = data.get('userId')
    dept_id = data.get('deptId')
    page = data.get('page')
    per_page = data.get('per_page')
    role_info = SysRole.query.join(SysUserRole,SysRole.role_id==SysUserRole.role_id).join(SysUser,SysUser.user_id==SysUserRole.user_id).filter_by(user_id=user_id).first()
    if role_info.role_id in (1,1855189303667335169,1855189077904728066,1855188956748062721):
        sys_dept = SysDept.query.filter_by(dept_id=dept_id).first()
        if sys_dept.parent_id == 1:
            query = DataResources.query.filter_by(dept_id=dept_id)
        else:
            query = DataResources.query.filter_by(dept_id=sys_dept.parent_id)
    elif role_info.role_id in (1855188843279556609,):
        query = DataResources.query.join(DataResourcesAuth,(DataResources.id==DataResourcesAuth.data_resources_id)).filter_by(user_id=user_id)
    datasource_infos = query.paginate(page=page,per_page=per_page).items
    total = query.count()
    datasource_infos_list = []
    for datasource_info in datasource_infos:
        datasource_info = datasource_info.__dict__
        dept = SysDept.query.filter_by(dept_id=datasource_info.get('dept_id')).first()
        datasource_info['dept_name'] = dept.dept_name
        datasource_info['auth_user'] = DataResourcesAuth.query.filter_by(data_resources_id=datasource_info.get('id')).count()
        datasource_infos_list.append(datasource_info)
    datasource_infos_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                           datasource_infos_list]
    data = {
        "page":page,
        "per_page":per_page,
        "data":datasource_infos_list,
        "total":total
    }
    return jsonify({"code":200,"data":data})


@exploration_bp.route('/query/dept/resources', methods=['POST'])
@custom_jwt_required
def query_dept_resources():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    order = data.get('order', 'asc')
    sort_key = data.get('sort_key')
    dept_name = data.get('dept_name')
    query = SysDept.query.filter_by(parent_id=1,del_flag="0")
    if dept_name:
        query = SysDept.query.filter_by(parent_id=1,del_flag="0").filter(SysDept.dept_name.like(f"%{dept_name}%"))
    dept_infos = query.all()
    total = query.count()
    dept_infos_list = []
    for dept_info in dept_infos:
        dept_info = dept_info.__dict__
        dept_info['file_total'] = int(DataResources.query.filter_by(dept_id=dept_info.get('dept_id')).count())
        dept_info['dept_id'] = str(dept_info['dept_id'])
        dept_infos_list.append(dept_info)
    dept_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                       dept_infos_list]
    if sort_key:
        if order == 'asc':
            dept_infos_list = sorted(dept_infos_list, key=lambda x: x[sort_key])
        else:
            dept_infos_list = sorted(dept_infos_list, key=lambda x: x[sort_key], reverse=True)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    dept_infos_list = dept_infos_list[start_index:end_index]
    data = {
        "page": page,
        "per_page": per_page,
        "data": dept_infos_list,
        "total":total
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/delete/resources', methods=['POST'])
@custom_jwt_required
def delete_resources():
    data = request.get_json()
    resources_id = data.get('resources_id')
    resources_info = DataResources.query.filter_by(id=resources_id).first()
    db.session.delete(resources_info)
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/update/resources', methods=['POST'])
@custom_jwt_required
def update_resources():
    data = request.get_json()
    resources_id = data.get('resources_id')
    dept_id = data.get('dept_id')
    update_id = data.get('userId')
    resources_info = DataResources.query.filter_by(id=resources_id).first()
    resources_info.dept_id = dept_id
    resources_info.update_id = update_id
    resources_info.update_time = int(datetime.now().timestamp())
    db.session.commit()
    return jsonify({'code': 200})


@exploration_bp.route('/query/user', methods=['POST'])
@custom_jwt_required
def query_user():
    data = request.get_json()
    resources_id = data.get('resources_id')
    dept_id = data.get('dept_id')
    page = data.get('page')
    per_page = data.get('per_page')
    name_phone = data.get('name_phone')
    _sys_depts = SysDept.query.filter(SysDept.ancestors.contains(f",{dept_id}")).all()
    ids_list = [_sys_dept.dept_id for _sys_dept in _sys_depts]
    ids_list.append(dept_id)
    query = SysUser.query.filter(SysUser.dept_id.in_(ids_list)).filter_by(del_flag='0')
    if name_phone:
        query = SysUser.query.filter(SysUser.dept_id.in_(ids_list)).filter(
            or_(
                SysUser.nick_name.like(f"%{name_phone}%"),
                SysUser.phonenumber.like(f"%{name_phone}%")
            )
        ).filter_by(del_flag='0')
    user_infos = query.paginate(page=page, per_page=per_page).items
    total = query.count()
    user_infos_list = []
    auth_user_list = []
    for user_info in user_infos:
        user_info = user_info.__dict__
        dept_info = SysDept.query.filter_by(dept_id=user_info.get('dept_id')).first()
        if dept_info.parent_id == 1:
            unit_department = dept_info.dept_name + '/' + dept_info.dept_name
        else:
            ancestors = dept_info.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            unit_info = SysDept.query.filter_by(parent_id=1).filter(SysDept.ancestors.in_(ancestors)).first()
            unit_department = unit_info.dept_name + '/' + dept_info.dept_name
        user_info['unit_department'] = unit_department
        user_info['phonenumber'] = hide_middle_digits(user_info['phonenumber'])
        auth_user = DataResourcesAuth.query.filter_by(user_id=user_info.get('user_id'),data_resources_id=resources_id).first()
        if auth_user:
            auth_user_list.append(user_info)
            user_info['auth'] = True
        else:
            user_info['auth'] = False
        user_infos_list.append(user_info)
    user_infos_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                       user_infos_list]
    auth_user_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                       auth_user_list]
    data = {
        "page": page,
        "per_page": per_page,
        "data": user_infos_list,
        "auth_data":auth_user_list,
        "total":total
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/resources/auth', methods=['POST'])
@custom_jwt_required
def resources_auth():
    data = request.get_json()
    user_ids = data.get('user_ids')
    data_resources_id = data.get('data_resources_id')
    data_resources_auths = DataResourcesAuth.query.filter_by(data_resources_id=data_resources_id).all()
    for data_resources_auth in data_resources_auths:
        db.session.delete(data_resources_auth)
        db.session.commit()
    for user_id in user_ids:
        data_resources_auth = DataResourcesAuth(
            user_id=user_id,
            data_resources_id=data_resources_id
        )
        db.session.add(data_resources_auth)
    db.session.commit()
    return jsonify({'code': 200})

@exploration_bp.route('/judge/user/auth',methods=['POST'])
@custom_jwt_required
def judge_user_auth():
    data = request.get_json()
    user_id = data.get('user_id')
    data_resources_auth = DataResourcesAuth.query.filter_by(user_id=user_id).first()
    if data_resources_auth:
        return jsonify({"code":200,"auth":True})
    return jsonify({"code":200,"auth":False})


@exploration_bp.route('/download/resources', methods=['POST'])
@custom_jwt_required
def download_resources():
    data = request.get_json()
    data_resources_id = data.get('data_resources_id')
    data_resources = DataResources.query.filter_by(id=data_resources_id).first()
    data_resources.download_total += 1
    data_resources_download_log = DataResourcesDownloadLog(
        user_id=data.get('userId'),
        data_resources_id=data_resources_id
    )
    db.session.add(data_resources_download_log)
    db.session.commit()
    return send_file(data_resources.file_path,as_attachment=True,download_name=data_resources.file_name)


@exploration_bp.route('/query/download/record', methods=['POST'])
@custom_jwt_required
def query_download_record():
    data = request.get_json()
    data_resources_id = data.get('data_resources_id')
    page = data.get('page')
    per_page = data.get('per_page')
    query = DataResourcesDownloadLog.query.filter_by(data_resources_id=data_resources_id).order_by(DataResourcesDownloadLog.create_time.desc())
    data_resources_download_log_infos = query.paginate(page=page, per_page=per_page).items
    total = query.count()
    data_resources_download_log_infos_list = []
    for data_resources_download_log_info in data_resources_download_log_infos:
        data_resources_download_log_info = data_resources_download_log_info.__dict__
        user_info = SysUser.query.filter_by(user_id=data_resources_download_log_info.get('user_id')).first()
        dept_info = SysDept.query.filter_by(dept_id=user_info.dept_id).first()
        if dept_info.parent_id == 1:
            unit_department = dept_info.dept_name + '/' + dept_info.dept_name
        else:
            ancestors = dept_info.ancestors.split(',')
            ancestors = [i for i in ancestors if i != '']
            unit_info = SysDept.query.filter_by(parent_id=1).filter(SysDept.ancestors.in_(ancestors)).first()
            unit_department = unit_info.dept_name + '/' + dept_info.dept_name
        data_resources_download_log_info['unit_department'] = unit_department
        data_resources_download_log_info['download_person'] = user_info.nick_name
        data_resources_download_log_infos_list.append(data_resources_download_log_info)
    data_resources_download_log_infos_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                       data_resources_download_log_infos_list]
    data = {
        "page": page,
        "per_page": per_page,
        "data": data_resources_download_log_infos_list,
        "total":total
    }
    return jsonify({'code': 200, 'data': data})


@exploration_bp.route('/get/phone/number',methods=['POST'])
@custom_jwt_required
def get_phone_number():
    data = request.get_json()
    user_id = data.get('user_id')
    user_info = SysUser.query.filter_by(user_id=user_id).first()
    return jsonify({"code":200,"data":user_info.phonenumber})

