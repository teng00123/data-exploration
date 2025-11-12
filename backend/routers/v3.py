from flask import Blueprint, request
from backend.database.base import GenericCRUD
from backend.database.log import UserOperationLog, SendSMSLog
from backend.response.code import SuccessResponse, ErrorResponse, FileResponse
from backend.utils import Pagination
import pandas as pd
from io import BytesIO

router = Blueprint('log', __name__)


@router.route('/query/user/operation/log', methods=['POST'])
def user_operation_log():
    data = request.get_json()
    keys_to_filter = [
    'operation_type', 'result_code'
    ]
    vague_keys_to_filter = [
    'nick_name', 'user_name', 'phone', 'operation_time',
    'operation_url', 'result_message', 'ipaddress',
    'useragent', 'operation_details', 'operation_manage'

    ]
    filterdict = {key: data[key] for key in keys_to_filter if data.get(key) is not None}
    vague_filter_dict = {key: data[key] for key in vague_keys_to_filter if data.get(key) is not None}
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        user_operation_log = GenericCRUD.query_by_conditions(UserOperationLog,order_by='-created_at',filters=filterdict)
        for item in vague_filter_dict.keys():
            user_operation_log = [i for i in user_operation_log if (i.get(item) or '').find(vague_filter_dict[item]) !=-1]
        pagination = Pagination(user_operation_log, page, per_page)
        result['count'] = pagination.total
        result['data'] = pagination.get_items()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()

@router.post('/log/download')
def download_log():
    try:
        user_operation_log = GenericCRUD.query_by_conditions(UserOperationLog, order_by='-created_at')
        key_mapping = {
            'user_id': '用户ID',
            'user_name': '用户名',
            'nick_name': '操作人姓名',
            'phone': '手机号',
            'operation_type': '操作类型',
            'operation_time': '操作时间',
            'operation_details': '业务操作',
            'operation_manage': '服务管理',
            'ip_address': 'IP地址',
            'user_agent': '客户端信息',
            'result_code': '操作结果',
            'result_message': '操作结果描述',
            'duration_ms':'耗时(ms)',
            'operation_url':'操作URL',
            'request_params': '请求参数',
            'request_boby':'请求体'
        }
        translated_data = []
        for item in user_operation_log:
            translated_item = {key_mapping[key]: value for key, value in item.items() if key in key_mapping}
            translated_data.append(translated_item)
        df = pd.DataFrame(translated_data)
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        return FileResponse(excel_buffer, filename='user_operation_log.xlsx').to_response()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()

@router.post('/sms/log/query')
def sms_log_query():
    # TODO: 实现短信日志查询功能
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    keys_to_filter = [
    'operation_type', 'result_code'
    ]
    vague_keys_to_filter = [
    'nick_name', 'user_name', 'phone', 'operation_time',
    'operation_url', 'result_message', 'ipaddress',
    'useragent', 'operation_details', 'operation_manage'

    ]
    filterdict = {key: data[key] for key in keys_to_filter if data.get(key) is not None}
    vague_filter_dict = {key: data[key] for key in vague_keys_to_filter if data.get(key) is not None}
    result = {
        'page': page,
        'per_page': per_page,
    }
    try:
        sms_log = GenericCRUD.query_by_conditions(SendSMSLog,order_by='-created_at',filters=filterdict)
        for item in vague_filter_dict.keys():
            sms_log = [i for i in sms_log if (i.get(item) or '').find(vague_filter_dict[item]) !=-1]
        pagination = Pagination(sms_log, page, per_page)
        result['count'] = pagination.total
        result['data'] = pagination.get_items()
    except Exception as e:
        return ErrorResponse(error_data=str(e)).to_response()
    return SuccessResponse(data=result).to_response()