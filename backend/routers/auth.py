from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, verify_jwt_in_request
)
import uuid
import secrets
from flask import Blueprint, jsonify, request
from backend.database.oauth import ClientUserInfo, ClientSecretInfo
from backend.config import db
from backend.database.sys_model import SysUser, SysDept
from sqlalchemy import not_

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/client', methods=['POST'])
def client():
    data = request.get_json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    if ClientSecretInfo.query.filter_by(client_id=client_id, client_secret=client_secret,is_disable=False).first():
        client_user_info = ClientUserInfo.query.filter_by(client_id=client_id).first()
        user_id = client_user_info.user_id
        access_token = create_access_token(identity=user_id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'code': 401, 'msg': 'client_id or client_secret error'})

@auth_bp.route('/authorize', methods=['POST'])
def authorize():
    data = request.get_json()
    user_ids = data.get('user_id')
    client_user_info = ClientUserInfo.query.filter(ClientUserInfo.user_id.in_(user_ids)).first()
    if client_user_info:
        return jsonify({'code': 500, 'msg': '该用户存在密钥，请勿重复创建'})
    for user_id in user_ids:
        client_id = str(uuid.uuid4())
        # 生成安全的密钥
        client_secret = secrets.token_urlsafe(32)
        client_user_info = ClientUserInfo(user_id=user_id, client_id=client_id)
        client_secret_info = ClientSecretInfo(client_id=client_id, client_secret=client_secret)
        db.session.add(client_user_info)
        db.session.add(client_secret_info)
        db.session.commit()
    return jsonify({'code': 200,'msg':'操作成功'})

@auth_bp.route('/authorize/query', methods=['POST'])
def authorize_get():
    data = request.get_json()
    page = data.get('page',1)
    per_page = data.get('per_page',10)
    user_name = data.get('user_name',None)
    dept_id = data.get('dept_id',None)
    query = ClientUserInfo.query
    if user_name:
        query = ClientUserInfo.query.join(SysUser,SysUser.user_id==ClientUserInfo.user_id).filter(SysUser.nick_name.like(f'%{user_name}%'))
    if dept_id:
        dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag="0").all()]
        dept_ids.append(dept_id)
        query = ClientUserInfo.query.join(SysUser,SysUser.user_id==ClientUserInfo.user_id).filter(SysUser.dept_id.in_(dept_ids))
    if user_name and dept_id:
        dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id, del_flag="0").all()]
        dept_ids.append(dept_id)
        query = ClientUserInfo.query.join(SysUser,SysUser.user_id==ClientUserInfo.user_id).filter(SysUser.nick_name.like(f'%{user_name}%')).filter(SysUser.dept_id.in_(dept_ids))
    client_users = query.paginate(page=page, per_page=per_page).items
    data = {
        'page':page,
        'per_page':per_page,
        'count':query.count(),
        'data':[]
    }
    for client_user in client_users:
        client_secret = ClientSecretInfo.query.filter_by(client_id=client_user.client_id).first()
        user_info = SysUser.query.filter_by(user_id=client_user.user_id).first()
        dept_info = SysDept.query.filter_by(dept_id=user_info.dept_id).first()
        data['data'].append({'user_name': user_info.nick_name,'dept_name':dept_info.dept_name, 'client_id': client_user.client_id, 'client_secret': client_secret.client_secret,'is_disable':client_secret.is_disable})
    return jsonify({'code': 200,'msg':'ok','data':data})


@auth_bp.route('/dept/query', methods=['POST'])
def dept_query():
    data = request.get_json()
    dept_id = data.get('dept_id',None)
    query = db.session.query(SysDept).filter(SysDept.parent_id == 1)
    if dept_id:
        query = db.session.query(SysDept).filter(SysDept.parent_id == dept_id)
    data = {'data':[]}
    for dept in query.all():
        data['data'].append({
            'dept_id': str(dept.dept_id),
            'dept_name': dept.dept_name
        })
    return jsonify({'code': 200,'msg':'ok','data':data})

@auth_bp.route('/user/query', methods=['POST'])
def user_query():
    data = request.get_json()
    page = data.get('page',1)
    per_page = data.get('per_page',10)
    user_name = data.get('user_name',None)
    dept_id = data.get('dept_id',None)
    dept_ids = [i.dept_id for i in SysDept.query.all()]
    if dept_id:
        dept_ids = [i.dept_id for i in SysDept.query.filter_by(parent_id=dept_id,del_flag="0").all()]
        dept_ids.append(dept_id)
    user_ids = [i.user_id for i in ClientUserInfo.query.all()]
    query = db.session.query(SysUser).filter(SysUser.dept_id.in_(dept_ids)).filter_by(del_flag="0").filter(not_(SysUser.user_id.in_(user_ids)))
    if user_name:
        query = query.filter(SysUser.nick_name.like(f"%{user_name}%"))
    data = {
        'page':page,
        'per_page':per_page,
        'count':query.count(),
        'data':[]
    }
    for user in query.paginate(page=page, per_page=per_page).items:
        dept_info = SysDept.query.filter_by(dept_id=user.dept_id).first()
        data['data'].append({
            'user_id': str(user.user_id),
            'user_name': user.nick_name,
            'dept_name': dept_info.dept_name
        })
    return jsonify({'code': 200,'msg':'ok','data':data})

@auth_bp.route('/disable', methods=['POST'])
def disable():
    data = request.get_json()
    client_id = data.get('client_id')
    client_info = ClientSecretInfo.query.filter_by(client_id=client_id).first()
    if client_info:
        client_info.is_disable = True
        db.session.commit()
        return jsonify({'code': 200,'msg':'操作成功'})
    return jsonify({'code': 500,'msg':'操作失败'})

@auth_bp.route('/enable', methods=['POST'])
def enable():
    data = request.get_json()
    client_id = data.get('client_id')
    client_info = ClientSecretInfo.query.filter_by(client_id=client_id).first()
    if client_info:
        client_info.is_disable = False
        db.session.commit()
        return jsonify({'code': 200,'msg':'操作成功'})
    return jsonify({'code': 500,'msg':'error'})

@auth_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    client_id = data.get('client_id')
    client_info = ClientSecretInfo.query.filter_by(client_id=client_id).first()
    if client_info:
        client_user = ClientUserInfo.query.filter_by(client_id=client_id).first()
        db.session.delete(client_info)
        db.session.delete(client_user)
        db.session.commit()
        return jsonify({'code': 200,'msg':'操作成功'})
    return jsonify({'code': 500,'msg':'error'})

