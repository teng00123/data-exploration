from flask import Blueprint, jsonify,request
from sqlalchemy import func,or_

from backend.database.exploration_model import BelongSystem
from backend.database.directory import DataDirectory,DataDirectoryItem
from backend.database.sys_model import SysDept, DataType, ServiceObject

large_bp = Blueprint('large', __name__)

@large_bp.route('/overview',methods=['POST'])
def overview():
    data = request.get_json()
    type = data.get('type')
    no_dept_ids = [4, 1851507096929443842, 1861578281075449858, 1856162650240790529]
    system_total = BelongSystem.query.filter(BelongSystem.department_id.not_in (no_dept_ids)).count()
    data_directory_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter_by(build_directory=True).count()
    data_directory_item_total = DataDirectoryItem.query.join(DataDirectory,
                                                             DataDirectoryItem.data_directory_id == DataDirectory.id).filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).count()
    data_total = sum([int(i.data_zie) for i in DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).all() if i.data_zie !=None])
    data_total = int(data_total) if data_total else 0
    data_storage = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter_by(build_directory=True).with_entities(
        func.sum(DataDirectory.data_storage_capacity)).scalar()
    data_storage = int(data_storage) if data_storage else 0
    data = {
        "system_total": system_total,
        "data_directory_total": data_directory_total,
        "data_directory_item_total": data_directory_item_total,
        "data_total": data_total,
        "data_storage": data_storage
    }
    return jsonify({'code':'200','msg':'success','data':data})

@large_bp.route('/overview/dept',methods=['POST'])
def overview_dept():
    payload = request.get_json()
    dept_id = payload.get('dept_id')
    type = payload.get('type')
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id).all()]
    dept_ids.append(dept_id)
    system_query = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids))
    system_total = system_query.count()
    system_ids = [i.id for i in system_query.all()]
    data_directory_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter_by(build_directory=True).filter(DataDirectory.system_id.in_(system_ids)).count()
    data_directory_item_total = DataDirectoryItem.query.join(DataDirectory,
                                                             DataDirectoryItem.data_directory_id == DataDirectory.id).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(DataDirectory.build_directory==True).filter(DataDirectory.system_id.in_(system_ids)).count()
    data_total = sum([int(i.data_zie) for i in DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter_by(build_directory=True).filter(DataDirectory.system_id.in_(system_ids)).all() if i.data_zie != None])
    data_total = int(data_total) if data_total else 0
    data_storage = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter_by(build_directory=True).filter(DataDirectory.system_id.in_(system_ids)).with_entities(
        func.sum(DataDirectory.data_storage_capacity)).scalar()
    data_storage = int(data_storage) if data_storage else 0
    data = {
        "system_total": system_total,
        "data_directory_total": data_directory_total,
        "data_directory_item_total": data_directory_item_total,
        "data_total": data_total,
        "data_storage": data_storage
    }
    return jsonify({'code':'200','msg':'success','data':data})

@large_bp.route('/dept',methods=['POST'])
def dept_system():
    data = request.get_json()
    type = data.get('type')
    query = SysDept.query.filter_by(parent_id='1', del_flag='0').filter(SysDept.dept_id != 4)
    dept_info_list = query.all()
    sorted_data = []
    for dept_info in dept_info_list:
        dept_ids_list = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_info.dept_id, del_flag='0').all()]
        dept_ids_list.append(dept_info.dept_id)
        system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids_list)).count()
        datasource_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).join(BelongSystem,
                                                                                                         BelongSystem.id == DataDirectory.system_id).filter(
            BelongSystem.department_id.in_(dept_ids_list)).count()
        sorted_data.append({
            'dept_name': dept_info.dept_name,
            'system_total': system_total,
            'datasource_total': datasource_total
        })
    return jsonify({'code':'200','msg':'success','data':sorted_data})

@large_bp.route('/system/analysis',methods=['POST'])
def system_analysis():
    data = request.get_json()
    type = data.get('type')
    system_total = BelongSystem.query.count()
    data = {
        'system_type': [],
        'service_object': [],
        'network_type': []
    }
    system_type = ['基础设施', '数据系统', '业务系统', '政务服务系统', '其他']
    for i in system_type:
        system_type_total = BelongSystem.query.filter(
            BelongSystem.system_type.like(f'%{i}%')).count()
        data['system_type'].append(
            {
                'name': i,
                'system': system_type_total,
                'percentage': round(system_type_total / system_total * 100, 2) if system_type_total != 0 else 0
            }
        )
    service_object = ['企业', '社会公众', '部门内部']
    for i in service_object:
        service_object_total = BelongSystem.query.filter(
            BelongSystem.service_object.like(f'%{i}%')).count()
        data['service_object'].append(
            {
                'name': i,
                'system': service_object_total,
                'percentage': round(service_object_total / system_total * 100, 2) if service_object_total != 0 else 0
            }
        )
    network_type = ['互联网', '电子政务外网', '电子政务内网', '行业专网', '电子政务外网和互联网']
    for i in network_type:
        network_type_total = BelongSystem.query.filter(
            BelongSystem.network == i).count()
        data['network_type'].append(
            {
                'name': i,
                'system': network_type_total,
                'percentage': round(network_type_total / system_total * 100, 2) if network_type_total != 0 else 0
            }
        )
    return jsonify({'code':'200','msg':'success','data':data})

@large_bp.route('/system/analysis/dept',methods=['POST'])
def system_analysis_dept():
    payload = request.get_json()
    type = payload.get('type')
    dept_id = payload.get('dept_id')
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id).all()]
    dept_ids.append(dept_id)
    system_total = BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).count()
    data = {
        'system_type': [],
        'service_object': [],
        'network_type': []
    }
    system_type = ['基础设施', '数据系统', '业务系统', '政务服务系统', '其他']
    for i in system_type:
        system_type_total = BelongSystem.query.filter(
            BelongSystem.system_type.like(f'%{i}%')).filter(BelongSystem.department_id.in_(dept_ids)).count()
        data['system_type'].append(
            {
                'name': i,
                'system': system_type_total,
                'percentage': round(system_type_total / system_total * 100, 2) if system_type_total != 0 else 0
            }
        )
    service_object = ['企业', '社会公众', '部门内部']
    for i in service_object:
        service_object_total = BelongSystem.query.filter(
            BelongSystem.service_object.like(f'%{i}%')).filter(BelongSystem.department_id.in_(dept_ids)).count()
        data['service_object'].append(
            {
                'name': i,
                'system': service_object_total,
                'percentage': round(service_object_total / system_total * 100, 2) if service_object_total != 0 else 0
            }
        )
    network_type = ['互联网', '电子政务外网', '电子政务内网', '行业专网', '电子政务外网和互联网']
    for i in network_type:
        network_type_total = BelongSystem.query.filter(
            BelongSystem.network == i).filter(BelongSystem.department_id.in_(dept_ids)).count()
        data['network_type'].append(
            {
                'name': i,
                'system': network_type_total,
                'percentage': round(network_type_total / system_total * 100, 2) if network_type_total != 0 else 0
            }
        )
    return jsonify({'code':'200','msg':'success','data':data})


@large_bp.route('/data_resource/analysis',methods=['POST'])
def data_resource_analysis():
    data = request.get_json()
    type = data.get('type')
    data_directory_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).count()
    data = {
        'ywy': [],
        'zty': [],
        'yw_object': [],
        'data_processing': [],
        'up_cycle': []
    }
    ywy_infos = DataType.query.filter_by(type="1").all()
    for ywy_info in ywy_infos:
        ywy_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.ywy_name.like(f"%{ywy_info.name}%")).count()
        data['ywy'].append(
            {
                'name': ywy_info.name,
                'data_resource': ywy_total,
                'percentage': round(ywy_total / data_directory_total * 100, 2) if ywy_total != 0 else 0
            }
        )
    zty_infos = DataType.query.filter_by(type="2").all()
    for zty_info in zty_infos:
        zty_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.zty_name.like(f"%{zty_info.name}%")).count()
        data['zty'].append(
            {
                'name': zty_info.name,
                'data_resource': zty_total,
                'percentage': round(zty_total / data_directory_total * 100, 2) if zty_total != 0 else 0
            }
        )
    service_infos = ServiceObject.query.all()
    for service_info in service_infos:
        service_object_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.ydx_name == service_info.name).count()
        data['yw_object'].append(
            {
                'name': service_info.name,
                'data_resource': service_object_total,
                'percentage': round(service_object_total / data_directory_total * 100, 2) if service_object_total != 0 else 0
            }
        )
    data_processings = ['原始数据','脱敏数据','标签数据','统计数据','融合数据']
    for data_processing in data_processings:
        data_processing_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.data_processing == data_processing).count()
        data['data_processing'].append(
            {
                'name': data_processing,
                'data_resource': data_processing_total,
                'percentage': round(data_processing_total / data_directory_total * 100, 2) if data_processing_total != 0 else 0
            }
        )
    up_cycles = ['实时','每日','每周','每月','每季度','每年','其他']
    for up_cycle in up_cycles:
        up_cycle_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.up_cycle == up_cycle).count()
        data['up_cycle'].append(
            {
                'name': up_cycle,
                'data_resource': up_cycle_total,
                'percentage': round(up_cycle_total / data_directory_total * 100, 2) if up_cycle_total != 0 else 0
            }
        )
    return jsonify({'code':'200','msg':'success','data':data})

@large_bp.route('/data_resource/analysis/dept',methods=['POST'])
def data_resource_analysis_dept():
    payload = request.get_json()
    dept_id = payload.get('dept_id')
    type = payload.get('type')
    dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id).all()]
    dept_ids.append(dept_id)
    system_ids = [i.id for i in BelongSystem.query.filter(BelongSystem.department_id.in_(dept_ids)).all()]
    data_directory_total = DataDirectory.query.filter_by(build_directory=True).filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(DataDirectory.system_id.in_(system_ids)).count()
    data = {
        'ywy': [],
        'zty': [],
        'yw_object': [],
        'data_processing': [],
        'up_cycle': []
    }
    ywy_infos = DataType.query.filter_by(type="1").all()
    for ywy_info in ywy_infos:
        ywy_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.ywy_name.like(f"%{ywy_info.name}%")).filter(DataDirectory.system_id.in_(system_ids)).count()
        data['ywy'].append(
            {
                'name': ywy_info.name,
                'data_resource': ywy_total,
                'percentage': round(ywy_total / data_directory_total * 100, 2) if ywy_total != 0 else 0
            }
        )
    zty_infos = DataType.query.filter_by(type="2").all()
    for zty_info in zty_infos:
        zty_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.zty_name.like(f"%{zty_info.name}%")).filter(DataDirectory.system_id.in_(system_ids)).count()
        data['zty'].append(
            {
                'name': zty_info.name,
                'data_resource': zty_total,
                'percentage': round(zty_total / data_directory_total * 100, 2) if zty_total != 0 else 0
            }
        )
    service_infos = ServiceObject.query.all()
    for service_info in service_infos:
        service_object_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.ydx_name == service_info.name).filter(DataDirectory.system_id.in_(system_ids)).count()
        data['yw_object'].append(
            {
                'name': service_info.name,
                'data_resource': service_object_total,
                'percentage': round(service_object_total / data_directory_total * 100, 2) if service_object_total != 0 else 0
            }
        )
    data_processings = ['原始数据', '脱敏数据', '标签数据', '统计数据', '融合数据']
    for data_processing in data_processings:
        data_processing_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.data_processing == data_processing).filter(DataDirectory.system_id.in_(system_ids)).count()
        data['data_processing'].append(
            {
                'name': data_processing,
                'data_resource': data_processing_total,
                'percentage': round(data_processing_total / data_directory_total * 100, 2) if data_processing_total != 0 else 0
            }
        )
    up_cycles = ['实时', '每日', '每周', '每月', '每季度', '每年', '其他']
    for up_cycle in up_cycles:
        up_cycle_total = DataDirectory.query.filter(or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.up_cycle == up_cycle).filter(DataDirectory.system_id.in_(system_ids)).count()
        data['up_cycle'].append(
            {
                'name': up_cycle,
                'data_resource': up_cycle_total,
                'percentage': round(up_cycle_total / data_directory_total * 100, 2) if up_cycle_total != 0 else 0
            }
        )
    return jsonify({'code':'200','msg':'success','data':data})

@large_bp.route('/dept/query', methods=['POST'])
def query_dept():
    payload = request.get_json()
    type = payload.get('type')
    if type == '1':
        down_depts = ['省粮食和储备局','四川省税务局','四川邮政管理局','四川地震局','四川气象局','四川测绘局']
        sys_dept_infos = SysDept.query.filter_by(parent_id=1).all()
        data = {'up_depts':[],'down_depts':[]}
        for sys_dept_info in sys_dept_infos:
            if sys_dept_info.dept_id != 4:
                if sys_dept_info.dept_name in down_depts:
                    data['down_depts'].append(
                        {
                            'name': sys_dept_info.dept_name,
                            'dept_id': str(sys_dept_info.dept_id)
                        }
                    )
                else:
                    data['up_depts'].append(
                        {
                            'name': sys_dept_info.dept_name,
                            'dept_id': str(sys_dept_info.dept_id)
                        }
                    )
        return jsonify({'code': '200', 'msg': 'success', 'data': data})
    elif type == '2':
        sys_dept_infos = SysDept.query.filter_by(parent_id=1).all()
        down_dept_infos = ['成都市','自贡市','攀枝花市','泸州市','德阳市','绵阳市','广元市','遂宁市','内江市','乐山市','南充市',
        '眉山市','宜宾市','广安市','达州市','雅安市','巴中市','资阳市','阿坝藏族羌族自治州','甘孜藏族自治州','凉山彝族自治州']
        data = {'up_depts': [], 'down_depts': []}
        for sys_dept_info in sys_dept_infos:
            if sys_dept_info.dept_id != 4:
                data['up_depts'].append(
                    {
                        'name': sys_dept_info.dept_name,
                        'dept_id': str(sys_dept_info.dept_id)
                    }
                )
        for dept_info in down_dept_infos:
            data['down_depts'].append(
                {
                    'name': dept_info,
                    'dept_id': dept_info
                }
        )
        return jsonify({'code':'200','msg':'success','data':data})