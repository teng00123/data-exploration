import json

from flask import Blueprint, jsonify, request, send_file, Response, send_from_directory
from backend.expand.pretreatment import load_execl
from backend.llm.openai import OpenAI,WelcomeMessage
from backend.expand.processing import processing_v1_result,processing_v2_result,generate_final_result,generate_check_final_result
from backend.config import config

llm_chat_bp = Blueprint('llm_chat', __name__)

def generate_data(data) -> str:
    for item in data:
        yield f"event:message\ndata:" + item

@llm_chat_bp.route('/AI_prediction/welcome', methods=['POST'])
def prediction_welcome():
    data = request.get_json()
    version = data.get('version')
    welcome_message = WelcomeMessage.get_welcome_message(version)
    return Response(generate_data(welcome_message), mimetype='text/plain')

@llm_chat_bp.route('/AI_prediction/v1', methods=['POST'])
def prediction_v1():
    file = request.files['file']
    process_list = load_execl(file)
    # TODO: 调用llm接口
    content = processing_v1_result(OpenAI(), process_list)
    # TODO: 处理结果
    file_path = generate_final_result(content,process_list)
    return send_file(file_path, as_attachment=True, download_name='AI分析字段模式1结果.xlsx',mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@llm_chat_bp.route('/AI_prediction/v2', methods=['POST'])
def prediction_v2():
    file = request.files['file']
    process_list = load_execl(file)
    # TODO: 调用llm接口
    content = processing_v2_result(OpenAI(), process_list)
    file_path = generate_final_result(content,process_list)
    return send_file(file_path, as_attachment=True, download_name='AI分析字段模式2结果.xlsx',mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@llm_chat_bp.route('/AI_prediction/check', methods=['POST'])
def prediction_v3():
    file = request.files['file']
    mode = request.form.get('mode')
    process_list = load_execl(file)
    # TODO: 调用llm接口
    if mode == 'v1':
        content = processing_v1_result(OpenAI(), process_list)
    elif mode == 'v2':
        content = processing_v2_result(OpenAI(), process_list)
    else:
        return jsonify({'code':203,'error': 'Invalid mode'})
    # TODO: 校验结果
    file_path = generate_check_final_result(content, process_list)
    return send_file(file_path, as_attachment=True, download_name='AI分析字段检查结果.xlsx',mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@llm_chat_bp.route('/AI_prediction/health', methods=['POST'])
def health_check():
    file = request.files['file']
    import pandas as pd
    excel_data = pd.read_excel(file, sheet_name="数据资源信息")

    # Convert the DataFrame to JSON format
    json_data = excel_data.to_json(orient='records', force_ascii=False)
    print(json_data)
    return jsonify({'code':200,'message':'success'})