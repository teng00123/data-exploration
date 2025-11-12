from datetime import datetime

from backend.config import db
from backend.database.base import BaseModel

class QualityInfo(db.Model):
    __tablename__ = 'quality_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quality_name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=True)
    execution_time = db.Column(db.String(255))
    cycle = db.Column(db.String(255))
    minute = db.Column(db.String(255))
    hour = db.Column(db.String(255))
    day = db.Column(db.String(255))
    week = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QualitySchedulerInfo(BaseModel):
    __tablename__ = 'quality_scheduler_info'

    table_id = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger)
    schedule_name = db.Column(db.String(255))
    minute = db.Column(db.String(255))
    hour = db.Column(db.String(255))
    day = db.Column(db.String(255))
    week = db.Column(db.String(255))
    method = db.Column(db.String(255))
    is_start = db.Column(db.Boolean, default=True)
    execute_time = db.Column(db.DateTime)

class QualityResult(db.Model):
    __tablename__ = 'quality_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scheduler_id = db.Column(db.String(255))
    dept_name = db.Column(db.String(255))
    data_none_total = db.Column(db.Integer)
    field_none_total = db.Column(db.Integer)
    datazie_total = db.Column(db.Integer)
    datastorage_total = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)