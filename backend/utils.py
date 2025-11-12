import json
import re
import os
from typing import Union
from cryptography.fernet import Fernet
from flask import Flask, g, request, jsonify
import jwt
from backend.template.mapping import dmdb_mapping, oracle_mapping, mysql_mapping, sqlite_mapping, pgsql_mapping
from backend.database.base import GenericCRUD
from backend.database.log import UserOperationLog
from backend.database.sys_model import SysUser
from functools import wraps
from backend.config import config
from datetime import datetime
from flask import jsonify, send_file, make_response, Response, stream_with_context
import subprocess
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import base64
import urllib.parse


def backup_mysql(host, port, user, password, database, is_docker=False, container_name=None):
    """备份MySQL数据库"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mysql_backup_{timestamp}.sql"
    filepath = os.path.join(config['UPLOAD_FOLDER'], filename)

    if is_docker and container_name:
        cmd = f"docker exec {container_name} mysqldump -h {host} -P {port} -u {user} -p{password} {database} > {filepath}"
    else:
        cmd = f"mysqldump -h {host} -P {port} -u {user} -p{password} {database} > {filepath}"

    subprocess.run(cmd, shell=True, check=True)
    return filepath


def backup_postgresql(host, port, user, password, database,filepath, is_docker=False, container_name=None, incremental=False):
    """备份PostgreSQL数据库"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mysql_backup_{timestamp}.sql"
    filepath = os.path.join(filepath, filename)
    if incremental:
        if is_docker and container_name:
            cmd = f"docker exec {container_name} pg_basebackup -h {host} -p {port} -U {user} -D - -Ft -P -R > {filepath}"
        else:
            cmd = f"pg_basebackup -h {host} -p {port} -U {user} -D - -Ft -P -R > {filepath}"
    else:
        if is_docker and container_name:
            cmd = f'docker exec {container_name} pg_dump "postgresql://{user}:{urllib.parse.quote_plus(password)}@{host}:{port}/{database}" > {filepath}'
        else:
            cmd = f'pg_dump "postgresql://{user}:{password}@{host}:{port}/{database}" > {filepath}'


    subprocess.run(cmd, shell=True, check=True)
    return filepath


def backup_sqlite(database_path):
    """备份SQLite数据库"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sqlite_backup_{timestamp}.db"
    filepath = os.path.join(config['UPLOAD_FOLDER'], filename)

    # SQLite备份就是直接复制文件
    import shutil
    shutil.copy2(database_path, filepath)
    return filepath


def aes_decrypt(encrypted_data: str, key: str = '1234567890123456', iv: str = '1234567890123456') -> str:
    """
    AES/CBC/PKCS7 解密
    :param encrypted_data: base64编码的加密字符串
    :param key: 16/24/32字节的密钥
    :param iv: 16字节的初始化向量
    :return: 解密后的明文字符串
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
    return decrypted.decode('utf-8')


def is_sql_injection_risky(sql):
    # 定义危险 SQL 关键字（排除 SELECT）
    dangerous_keywords = [
        r'\bINSERT\b',
        r'\bUPDATE\b',
        r'\bDELETE\b',
        r'\bDROP\b',
        r'\bALTER\b',
        r'\bCREATE\b',
        r'\bEXEC\b',
        r'\bEXECUTE\b',
        r'\bUNION\b',
        r'\bTRUNCATE\b',
        r'\bGRANT\b',
        r'\bREVOKE\b',
    ]

    # 定义常见 SQL 注入模式
    injection_patterns = [
        r';--',          # SQL 注释
        r'OR\s+1\s*=\s*1',  # 永真条件
        r'AND\s+1\s*=\s*1', # 永真条件
        r'\'\s*OR\s*\'1\'\s*=\s*\'1',  # 字符串形式的 OR 1=1
        r'UNION\s+SELECT',  # UNION 注入
        r'WAITFOR\s+DELAY',  # 时间延迟注入
        r'SLEEP\s*\(',      # MySQL 时间延迟注入
        r'XOR\s+1\s*=\s*1',  # XOR 注入
        r'IF\s*\(',         # 条件注入
        r'BENCHMARK\s*\(',  # MySQL 基准测试注入
    ]

    # 检查是否包含危险关键字（排除 SELECT）
    for pattern in dangerous_keywords:
        if re.search(pattern, sql, re.IGNORECASE):
            return True  # 检测到危险 SQL 操作

    # 检查是否包含 SQL 注入模式
    for pattern in injection_patterns:
        if re.search(pattern, sql, re.IGNORECASE):
            return True  # 检测到 SQL 注入模式

    return False  # 未检测到风险

def hide_middle_digits(phone_number):
    # 检查手机号码是否为11位数字
    if len(phone_number) != 11 or not phone_number.isdigit():
        return "输入的手机号码格式不正确。"

    # 隐藏中间四位数字
    hidden_number = phone_number[:3] + '****' + phone_number[7:]

    return hidden_number
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# # 从文件或环境变量中读取密钥
# with open(BASE_DIR + '/secret.key', 'rb') as key_file:
#     key = key_file.read()
key = "GHiC1UXbXbu3tBN-x-K8ubLZdKImj-QzgR0Nmii2MYQ="
cipher_suite = Fernet(key)

# 加密
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

# 解密函数
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def process_field_type(
        field_type_str: Union[str],
        database_type: Union[str]) -> tuple:
    if database_type == 'dmdb':
        mapping = dmdb_mapping
        return dm_exec(field_type_str, mapping)
    if database_type == 'mysql':
        mapping = mysql_mapping
    if database_type == 'postgresql':
        mapping = pgsql_mapping
    if database_type == 'oracle':
        mapping = oracle_mapping
    if database_type == 'sqlite':
        mapping = sqlite_mapping
    # Remove collation part
    field_type_str = field_type_str.split('COLLATE')[0].strip()

    # Split to get type and length
    if '(' in field_type_str:
        type_part, length_part = field_type_str.split('(')
        length = length_part.rstrip(')')
    else:
        type_part = field_type_str
        length = None

    # Map to Chinese
    chinese_type = mapping.get(type_part, type_part)

    return chinese_type, length


def dm_exec(
        field_type: Union[str],
        mapping: Union[dict]) -> tuple:
    # 提取字段类型和长度
    full_type = field_type[0]
    # 找到第一个数字的位置
    number_index = re.search(r'\d', full_type).start()
    # 分割类型和长度
    field = full_type[:number_index]
    length = full_type[number_index:]

    # 映射到中文类型
    chinese_type = mapping.get(field, field)  # 如果没有映射，则使用原字段类型

    # 打印结果
    return chinese_type, length


# 自定义装饰器来覆盖默认的JWT验证行为
def custom_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 从自定义头部获取token
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({'message': 'Token is missing!', 'code': 401})
        try:
            payload = jwt.decode(token, config.get('SECRET_KEY'), algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Invalid token!', 'code': 401})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!', 'code': 401})
        # 调用原始视图函数
        return fn(*args, **kwargs)

    return wrapper

# 自定义装饰器来记录用户操作
def record_user_operation(operation_type,operation_details,operation_manage):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 假设用户ID和用户名存储在 session 中，或者你可以根据实际情况获取
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, config.get('SECRET_KEY'), algorithms=['HS256'])
            user_id = payload.get('userId')
            user_info = GenericCRUD.query_by_conditions(SysUser, filters={'user_id':user_id},first=True)
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            # 获取操作前的当前时间
            start_time = datetime.utcnow()
            # 执行原始函数
            response = func(*args, **kwargs)

            # 获取操作后的当前时间
            end_time = datetime.utcnow()
            # 判断是否是文件流响应
            if isinstance(response, Response) and response.direct_passthrough:
                result_message = "[文件流响应，不记录内容]"
                result_code = 'success'
            else:
                result_message = str(response.data) if hasattr(response, 'data') else "[无响应内容]"
                response_data = json.loads(response.data.decode('utf-8'))
                result_code = 'success' if response_data.get('code') == 200 else 'fail'
            # 计算操作持续时间
            duration = (end_time - start_time).total_seconds() * 1000  # 毫秒
            GenericCRUD.create(
                UserOperationLog,
                user_id=user_id,
                user_name=user_info.get('user_name'),
                nick_name=user_info.get('nick_name'),
                phone=user_info.get('phonenumber'),
                operation_type=operation_type,
                operation_manage=operation_manage,
                operation_time=start_time,
                operation_details=operation_details,  # 或者其他你想要记录的详情
                ip_address=ip_address,
                user_agent=request.headers.get('User-Agent'),
                result_code=result_code,
                duration_ms=duration,
                result_message=result_message,
                operation_url=request.path,
                request_params=json.dumps(request.args.to_dict()),
                request_boby=json.dumps(request.get_json(), ensure_ascii=False) if request.get_json() else None,
            )
            return response
        return wrapper

    return decorator


class Pagination:
# 定义一个初始化函数，用于初始化分页器
    def __init__(self, items, page, per_page):
        # 将传入的items赋值给self.items
        self.items = items
        # 将传入的page赋值给self.page
        self.page = page
        # 将传入的per_page赋值给self.per_page
        self.per_page = per_page
        # 计算items的总数，并赋值给self.total
        self.total = len(items)

    # 获取当前页面的数据
    def get_items(self):
        # 计算起始位置
        start = (self.page - 1) * self.per_page
        # 计算结束位置
        end = start + self.per_page
        # 返回当前页面的数据
        return self.items[start:end]

    def has_prev(self):
        # 判断当前页码是否大于1，如果是，则返回True，否则返回False
        return self.page > 1

    def has_next(self):
        # 判断当前页数乘以每页显示的条数是否小于总条数
        return (self.page * self.per_page) < self.total

    def prev_page(self):
        # 如果当前页有上一页，则返回上一页的页码，否则返回None
        return self.page - 1 if self.has_prev() else None

    def next_page(self):
        # 如果有下一页，则返回当前页码加1，否则返回None
        return self.page + 1 if self.has_next() else None

    def total_pages(self):
        # 计算总页数
        return (self.total + self.per_page - 1) // self.per_page

    # 筛选功能
    def filter_items(self, filter_func):
        # 应用筛选函数对items进行筛选
        self.items = list(filter_func(item) for item in self.items)
        # 重新计算总数
        self.total = len(self.items)

    # 排序功能
    def sort_items(self, sort_key, reverse):
        # 应用排序函数对items进行排序
        self.items.sort(sort_key, reverse=reverse)
        # 重新计算总数
        self.total = len(self.items)


if __name__ == '__main__':

    pagination = Pagination([{"name":1}, {"name":2}, {"name":3}, {"name":4}, {"name":5}], 1,2)
    print(pagination.get_items())
    print(pagination.filter_items('name'))