from flask import Blueprint,jsonify,request
from sqlalchemy import and_
from backend.database.sys_model import SysDept, SysRole, SysUserRole, SysUser
from backend.database.exploration_model import BelongSystem
from backend.utils import custom_jwt_required

dept_bp = Blueprint('dept', __name__)


@dept_bp.route('/belonging_department',methods=['GET'])
@custom_jwt_required
def get_belonging_department():
    dept_id = request.args.get('dept_id')
    user_id = request.args.get('user_id',"1")
    sys_role = SysRole.query.join(SysUserRole, SysRole.role_id == SysUserRole.role_id).join(SysUser,
                                                                                            SysUser.user_id == SysUserRole.user_id).filter_by(
        user_id=user_id).first()
    sys_user = SysUser.query.filter_by(user_id=user_id).first()
    if sys_role.role_id in (1,1855189077904728066) and int(dept_id)==int(sys_user.dept_id):
        dept_id = "1"
    query = SysDept.query.filter_by(parent_id=dept_id)
    department_infos = query.all()
    department_list = [department_info.__dict__ for department_info in department_infos]
    department_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                                   department_list]
    return jsonify({'code':200,'data':department_list})

@dept_bp.route('/belonging_department/system',methods=['POST'])
@custom_jwt_required
def belonging_department_system():
    data = request.get_json()
    belong_system_id = data.get('belong_system_id')
    dept_id = data.get('dept_id')
    belong_system = BelongSystem.query.filter_by(id=belong_system_id).first()
    sys_dept = SysDept.query.filter_by(dept_id=belong_system.department_id).first()
    if sys_dept.parent_id == 1:
        query = SysDept.query.filter_by(parent_id=belong_system.department_id,del_flag='0')
    else:
        query = SysDept.query.filter_by(parent_id=sys_dept.parent_id,del_flag='0')
    if dept_id:
        query = query.filter_by(parent_id=dept_id,del_flag='0')
    department_infos = query.all()
    department_list = [department_info.__dict__ for department_info in department_infos]
    department_list = [{k: str(v) for k, v in info.items() if k != '_sa_instance_state'} for info in
                                   department_list]
    return jsonify({'code':200,'data':department_list})