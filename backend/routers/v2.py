from flask import Blueprint, request
from backend.service.v2_service import V2_Service
from backend.response.code import SuccessResponse,ErrorResponse

router = Blueprint('monitor', __name__)

@router.post('/data/scanning/status')
def data_scanning_status():
    try:
        result = V2_Service.get_data_scanning_status()
    except Exception as e:
        return ErrorResponse(str(e)).to_response()
    return SuccessResponse(result).to_response()

@router.post('/data/scanning/progress')
def data_scanning_progress():
    try:
        result = V2_Service.get_scaning_progress()
    except Exception as e:
        return ErrorResponse(str(e)).to_response()
    return SuccessResponse(result).to_response()

@router.post('/sharing/management/statistical/analysis/title')
def sharing_management_statistical_analysis_title():
    """共享管理统计分析标题"""
    data = request.get_json()
    try:
        result = V2_Service.get_sharing_management_statistical_analysis_title()
    except Exception as e:
        return ErrorResponse(str(e)).to_response()
    return SuccessResponse(result).to_response()