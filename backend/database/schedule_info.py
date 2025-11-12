from backend.config import db
from datetime import datetime


class ScheduleInfo(db.Model):
    __tablename__ = 'biz_schedule_info'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    datasource_id = db.Column(db.BigInteger, db.ForeignKey('biz_datasource_info.id', ondelete='CASCADE'),
                                   nullable=True)  # 数据源id
    schedule_name = db.Column(db.String(255))
    minute = db.Column(db.String(255))
    hour = db.Column(db.String(255))
    day = db.Column(db.String(255))
    week = db.Column(db.String(255))
    name = db.Column(db.String(255))
    method = db.Column(db.String(255))
    create_id = db.Column(db.BigInteger)
    department_id = db.Column(db.BigInteger)
    is_start = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.String(255), default=lambda :int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda :int(datetime.now().timestamp()),onupdate=lambda :int(datetime.now().timestamp()))

class ScheduleExecute(db.Model):
    __tablename__ = 'biz_schedule_execute'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    datasource_id = db.Column(db.BigInteger, db.ForeignKey('biz_datasource_info.id', ondelete='CASCADE'),
                                   nullable=True)  # 数据源id
    schedule_id = db.Column(db.BigInteger, db.ForeignKey('biz_schedule_info.id', ondelete='CASCADE'),
                                   nullable=True)  # 数据源id
    schedule_name = db.Column(db.String(255))
    schedule_time = db.Column(db.String(255))
    end_time = db.Column(db.String(255))
    time_consuming = db.Column(db.String(255))
    schedule_status = db.Column(db.String(255))
    failure_reason = db.Column(db.Text)
    create_time = db.Column(db.String(255), default=lambda :int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda :int(datetime.now().timestamp()),onupdate=lambda :int(datetime.now().timestamp()))
