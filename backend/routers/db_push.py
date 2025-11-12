import uuid
import random
from datetime import datetime

from flask import Blueprint, jsonify, request
from backend.config import db
from backend.database.db_push import DbPushTable, DbPushField
from backend.database.directory import DataDirectory, DataDirectoryItem
from backend.database.exploration_model import BelongSystem,TableInfo,FieldInfo
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, verify_jwt_in_request
)

from backend.database.sys_model import SysUser, SysDept

db_push_bp = Blueprint('db_push', __name__)


@db_push_bp.route('/data-table', methods=['POST'])
@jwt_required()
def data_table():
    data = request.get_json()
    system_name = data.get('systemName')
    table_ename = data.get('tableEName')
    table_cname = data.get('tableCName')
    data_item_cname = data.get('dataItemCName')
    data_item_ename = data.get('dataItemEName')
    data_item_type = data.get('dataItemType')
    data_item_length = data.get('dataItemLength')
    data_item_key = data.get('dataItemKey')
    data_item_empty = data.get('dataItemEmpty')
    data_item_default = data.get('dataItemDefault')
    data_item_auto = data.get('dataItemAuto')
    user_id = get_jwt_identity()
    user_info = SysUser.query.filter_by(user_id=user_id).first()
    dept_info = SysDept.query.filter_by(dept_id=user_info.dept_id).first()
    if dept_info.parent_id==1:
        dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=user_info.dept_id)]
        dept_ids.append(dept_info.dept_id)
    else:
        dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_info.parent_id)]
        dept_ids.append(dept_info.parent_id)
    belong_system = BelongSystem.query.filter_by(system_name=system_name).filter(BelongSystem.department_id.in_(dept_ids)).first()
    if belong_system is None:
        return jsonify({'code': 101,'msg':'您所在的单位下所属系统不存在,请检查信息系统名称', 'data': {}})
    check_table = DbPushTable.query.filter_by(system_id=belong_system.id, table_name=table_ename).first()
    if check_table is None:
        db_push_table = DbPushTable(
            system_id=belong_system.id,
            system_name=system_name,
            table_name=table_ename,
            table_comment=table_cname,
            create_id=user_info.user_id
        )
        db.session.add(db_push_table)
        db.session.flush()
        db_push_field = DbPushField(
            table_id=db_push_table.id,
            field_name=data_item_ename,
            field_comment=data_item_cname,
            field_type=data_item_type +'('+ data_item_length +')',
            is_primary_key=data_item_key,
            is_nullable=data_item_empty,
            default=data_item_default,
            is_autoincrement=data_item_auto,
        )
        db.session.add(db_push_field)
        id = random.randint(10 ** 17, 10 ** 18 - 1)
        data_directory = DataDirectory(
            id=id,
            table_id=db_push_table.id,
            create_id=user_info.user_id,
            status=1,
            system_id=belong_system.id,
            cn_name=table_cname,
            contents_code=str(uuid.uuid4()),
            en_name=table_ename,
            dept_id=user_info.dept_id,
            data_provider=dept_info.dept_name,
            history=False,
            build_directory=True,
            data_version=1,
            main_version_id=id,
            data_source_mode='数据对接',
            create_time=datetime.now()
        )
        db.session.add(data_directory)
        db.session.flush()
        data_directory_item = DataDirectoryItem(
            id=random.randint(10 ** 17, 10 ** 18 - 1),
            table_info_id=db_push_table.id,
            field_id=db_push_field.id,
            en_name=data_item_ename,
            item_name=data_item_cname,
            item_type=data_item_type +'('+ data_item_length +')',
            primary_keys=data_item_key,
            data_directory_id=data_directory.id,
        )
        db.session.add(data_directory_item)
        db.session.commit()
        return jsonify({'code': 100,'msg':f'添加表{table_ename}成功,添加字段{data_item_ename}成功', 'data': {}})
    else:
        data_directory = DataDirectory.query.filter_by(table_id=check_table.id,system_id=belong_system.id).first()
        data_directory.cn_name = table_cname
        check_table.table_comment = table_cname
        check_table.system_name = system_name
        check_field = DbPushField.query.filter_by(table_id=check_table.id,field_name=data_item_ename).first()
        if check_field:
            data_directory_item = DataDirectoryItem.query.filter_by(table_info_id=check_table.id,field_id=check_field.id).first()

            check_field.field_comment = data_item_cname
            check_field.field_type = data_item_type +'('+ data_item_length +')'
            check_field.is_primary_key = data_item_key
            check_field.is_nullable = data_item_empty
            check_field.default = data_item_default
            check_field.is_autoincrement = data_item_auto
            data_directory_item.item_name = data_item_cname
            data_directory_item.item_type = data_item_type +'('+ data_item_length +')'
            data_directory_item.primary_keys = data_item_key
            db.session.commit()
            return jsonify({'code': 100,'msg':f'更新字段{data_item_ename}成功', 'data': {}})
        db_push_field = DbPushField(
            table_id=check_table.id,
            field_name=data_item_ename,
            field_comment=data_item_cname,
            field_type=data_item_type +'('+ data_item_length +')',
            is_primary_key=data_item_key,
            is_nullable=data_item_empty,
            default=data_item_default,
            is_autoincrement=data_item_auto,
        )
        db.session.add(db_push_field)
        db.session.flush()
        data_directory_item = DataDirectoryItem(
            id=random.randint(10 ** 17, 10 ** 18 - 1),
            table_info_id=check_table.id,
            field_id=db_push_field.id,
            en_name=data_item_ename,
            item_name=data_item_cname,
            item_type=data_item_type +'('+ data_item_length +')',
            primary_keys=data_item_key,
            data_directory_id=data_directory.id,
        )
        db.session.add(data_directory_item)
        db.session.commit()
        return jsonify({'code': 100,'msg':f'添加字段{data_item_ename}成功', 'data': {}})

@db_push_bp.route('/data-size-total', methods=['POST'])
@jwt_required()
def data_size_total():
    data = request.get_json()
    system_name = data.get("systemName")
    table_ename = data.get("tableEName")
    db_number = data.get("dBNumber")
    user_id = get_jwt_identity()
    db_push_table = DbPushTable.query.filter_by(system_name=system_name, table_name=table_ename,create_id=user_id).first()
    if db_push_table is None:
        return jsonify({'code': 101,'msg':'数据表不存在', 'data': {}})
    data_directory = DataDirectory.query.filter_by(table_id=db_push_table.id,data_source_mode='数据对接').first()
    db_push_table.db_number = db_number
    data_directory.data_zie = db_number
    db.session.commit()
    return jsonify({'code': 100,'msg':'操作成功', 'data': {}})

@db_push_bp.route('/data-total', methods=['POST'])
@jwt_required()
def data_total():
    data = request.get_json()
    system_name = data.get('systemName')
    table_ename = data.get('tableEName')
    storage_capacity = data.get('storageCapacity')
    user_id = get_jwt_identity()
    db_push_table = DbPushTable.query.filter_by(system_name=system_name, table_name=table_ename,create_id=user_id).first()
    if db_push_table is None:
        return jsonify({'code': 101,'msg':'数据表不存在', 'data': {}})
    data_directory = DataDirectory.query.filter_by(table_id=db_push_table.id,data_source_mode='数据对接').first()
    db_push_table.storage_capacity = storage_capacity
    data_directory.data_storage_capacity=storage_capacity
    db.session.commit()
    return jsonify({'code': 100,'msg':'操作成功', 'data': {}})

