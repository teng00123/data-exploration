from flask import Blueprint, request
from backend.database.base import GenericCRUD
from backend.database.log import UserOperationLog
from backend.database.management import VariableManageInfo
from backend.response.code import SuccessResponse, ErrorResponse
from backend.utils import Pagination

router = Blueprint('management', __name__)

@router.post('/variable/manage/create')
def create_variable():
    data = request.get_json()
    variable_name = data.get('variable_name')
    variable_cname = data.get('variable_cname')
    variable_value = data.get('variable_value')
    variable_desc = data.get('variable_desc')
    try:
        GenericCRUD.create(VariableManageInfo,variable_name=variable_name,variable_cname=variable_cname, variable_value=variable_value, variable_desc=variable_desc)
        return SuccessResponse(data='创建成功').to_response()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()

@router.post('/variable/manage/query')
def get_variable_query():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    variable_name = data.get('variable_name')
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        variable_info = GenericCRUD.query_by_conditions(VariableManageInfo)
        if variable_name:
            variable_info = [i for i in variable_info if i.get('variable_name').find(variable_info) != -1]
        result_data = Pagination(variable_info, page, per_page)
        result['data'] = result_data.get_items()
        result['count'] = result_data.total
        return SuccessResponse(data=result).to_response()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()

@router.post('/variable/manage/update')
def update_variable():
    data = request.get_json()
    variable_id = data.get('variable_id')
    variable_name = data.get('variable_name')
    variable_value = data.get('variable_value')
    variable_desc = data.get('variable_desc')
    try:
        GenericCRUD.update(VariableManageInfo, variable_id, variable_name=variable_name, variable_value=variable_value, variable_desc=variable_desc)
        return SuccessResponse(data='更新成功').to_response()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()

@router.post('/variable/manage/delete')
def delete_variable():
    data = request.get_json()
    variable_id = data.get('variable_id')
    try:
        GenericCRUD.delete(VariableManageInfo, variable_id)
        return SuccessResponse(data='删除成功').to_response()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()