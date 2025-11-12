from flask import Blueprint, request
from backend.database.base import GenericCRUD
from backend.database.exploration_model import DatasourceInfo
from backend.response.code import SuccessResponse, ErrorResponse
from backend.utils import Pagination
from backend.utils import backup_postgresql,backup_mysql,backup_sqlite
import os
from cryptography.fernet import Fernet

router = Blueprint('backups', __name__)

key = "GHiC1UXbXbu3tBN-x-K8ubLZdKImj-QzgR0Nmii2MYQ="
cipher_suite = Fernet(key)

# 解密函数
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()


@router.route('/backup', methods=['POST'])
def backup():
    data = request.get_json()
    datasource_id = data.get('datasource_id')
    backup_type = data.get('backup_type')
    backup_path = data.get('backup_path','/root/xshl-data-exploration-python/backend/')
    incremental = data.get('incremental')
    is_docker = data.get('is_docker')
    container_name = data.get('container_name') if is_docker else None
    try:
        datasource_info = GenericCRUD.query_by_conditions(DatasourceInfo, filters={'id': datasource_id},first=True)
        db_type = datasource_info.get('database_type')
        database_address = datasource_info.get('database_address').split(':')
        host = database_address[0]
        port = database_address[1]
        user = datasource_info.get('database_username')
        password = decrypt_password(datasource_info.get('database_password'))
        database = datasource_info.get('database_name')

        if db_type == 'mysql':
            filepath = backup_mysql(host, port, user, password, database, is_docker, container_name)

        elif db_type == 'postgresql':
            filepath = backup_postgresql(host, port, user, password, database,backup_path, is_docker, container_name, incremental)

        elif db_type == 'sqlite':
            database_path = request.form.get('sqlite_path')
            filepath = backup_sqlite(database_path)
        result = {
            'success': True,
            'message': '备份成功！',
            'filename': os.path.basename(filepath),
            'download_url': f'/download/{os.path.basename(filepath)}'
        }
        return SuccessResponse(data=result).to_response()

    except Exception as e:
        return ErrorResponse(str(e)).to_response()
