from backend.config import db
from backend.database.base import BaseModel
import datetime

class UserOperationLog(BaseModel):
    __tablename__ = 'user_operation_log'

    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    user_name = db.Column(db.String(50), comment='用户名')
    nick_name = db.Column(db.String(50), comment='操作人姓名')
    phone = db.Column(db.String(50), comment='用户手机号')
    operation_type = db.Column(db.String(50), nullable=False, comment='操作类型') # 操作类型，如登录、登出、数据查询等
    operation_time = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow,comment='操作时间') # 操作时间
    operation_details = db.Column(db.Text, comment='业务操作') # 操作详情，如查询的SQL语句、更新的数据等
    operation_manage = db.Column(db.Text, comment='服务管理') # 操作详情，如查询的SQL语句、更新的数据等
    ip_address = db.Column(db.String(50), comment='操作的IP地址') # 操作的IP地址
    user_agent = db.Column(db.String(255), comment='操作的浏览器信息') # 操作的浏览器信息
    result_code = db.Column(db.String(50), comment='操作结果') # 操作结果，如成功、失败等
    result_message = db.Column(db.Text, comment='操作结果信息') # 操作结果信息，如错误信息等
    duration_ms = db.Column(db.Integer, comment='操作耗时，单位为毫秒') # 操作耗时，单位为毫秒
    operation_url = db.Column(db.String(255), comment='操作URL') # 操作URL
    request_params = db.Column(db.Text, comment='请求参数') # 请求参数
    request_boby = db.Column(db.Text, comment='请求体') # 请求体

class SendSMSLog(BaseModel):
    __tablename__ = 'send_sms_log'

    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    nick_name = db.Column(db.String(50), comment='操作人姓名')
    phone = db.Column(db.String(50), comment='用户手机号')
    department = db.Column(db.String(255), comment='所属部门')  # 所属部门
    belonging_department = db.Column(db.String(255), comment='所属处室')  # 所属处室
    sms_type = db.Column(db.String(50), nullable=False, comment='短信类型') # 短信类型，如验证码、通知等
    sms_content = db.Column(db.Text, comment='短信内容') # 短信内容
    send_time = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow,comment='发送时间') # 发送时间
    send_status = db.Column(db.String(50), comment='发送状态') # 发送状态，如成功、失败等