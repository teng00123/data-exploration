from backend.config import db
from backend.database.base import BaseModel
from sqlalchemy import Enum

class QualityReportResult(BaseModel):
    __tablename__ = 'quality_report_result'

    execute_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    quality_table_name = db.Column(db.String(255))
    repeatability = db.Column(db.Float) # 唯一性
    integrity = db.Column(db.Float) # 完整性
    accuracy = db.Column(db.Float) # 准确性
    consistency = db.Column(db.Float) # 一致性
    total = db.Column(db.Float)

class QualityAccuracy(BaseModel):
    __tablename__ = 'quality_accuracy'

    execute_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    quality_table_name = db.Column(db.String(255))
    quality_field_name = db.Column(db.Text)
    count = db.Column(db.BigInteger)
    problem_lines = db.Column(db.BigInteger)
    score = db.Column(db.Float)
    rule_id = db.Column(db.BigInteger)
    execute_log = db.Column(db.Text)

class QualityConsistency(BaseModel):
    __tablename__ = 'quality_consistency'

    execute_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    quality_table_name = db.Column(db.String(255))
    quality_field_name = db.Column(db.Text)
    count = db.Column(db.BigInteger)
    problem_lines = db.Column(db.BigInteger)
    score = db.Column(db.Float)
    rule_id = db.Column(db.BigInteger)
    execute_log = db.Column(db.Text)

class QualityRepeatability(BaseModel):
    __tablename__ = 'quality_repeatability'

    execute_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    quality_table_name = db.Column(db.String(255))
    quality_field_name = db.Column(db.Text)
    count = db.Column(db.BigInteger)
    problem_lines = db.Column(db.BigInteger)
    score = db.Column(db.Float)
    rule_id = db.Column(db.BigInteger)
    execute_log = db.Column(db.Text)

class QualityIntegrity(BaseModel):
    __tablename__ = 'quality_integrity'

    execute_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    quality_table_name = db.Column(db.String(255))
    quality_field_name = db.Column(db.String(255))
    count = db.Column(db.BigInteger)
    problem_lines = db.Column(db.BigInteger)
    score = db.Column(db.Float)
    rule_id = db.Column(db.BigInteger)
    execute_log = db.Column(db.Text)

class QualityTimeliness(BaseModel):
    __tablename__ = 'quality_timeliness'

    execute_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    quality_table_name = db.Column(db.String(255))
    result = db.Column(db.Text)
    timeliness = db.Column(db.Integer)

class QualityExecute(BaseModel):
    __tablename__ = 'quality_execute'

    schedule_name = db.Column(db.String(255))
    schedule_id = db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    quality_table_id = db.Column(db.BigInteger)
    quality_field_id = db.Column(db.BigInteger)
    rule_type = db.Column(db.String(255))
    execute_result = db.Column(db.Text)
    execute_status = db.Column(db.String(255))
    execute_time = db.Column(db.DateTime)

class QualityNormative(BaseModel):
    __tablename__ = 'quality_normative'

    execute_id=db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    quality_table_id = db.Column(db.BigInteger)
    table_no_comment = db.Column(db.Integer)
    field_no_comment = db.Column(db.Integer)
    field_count = db.Column(db.Integer)
    is_have_primary_keys = db.Column(db.Boolean)

class QualityNormativeDetail(BaseModel):
    __tablename__ = 'quality_normative_detail'

    execute_id=db.Column(db.BigInteger)
    database_id = db.Column(db.BigInteger)
    quality_table_id = db.Column(db.BigInteger)
    quality_field_id = db.Column(db.BigInteger)
    field_comment = db.Column(db.Text)
    field_type = db.Column(db.String(255))
    is_primary_key = db.Column(db.Boolean)
    field_name = db.Column(db.String(255))