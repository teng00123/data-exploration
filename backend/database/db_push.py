from datetime import datetime

from backend.config import db

class DbPushTable(db.Model):
    __tablename__ = 'db_push_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(255), nullable=False)
    table_comment = db.Column(db.String(255), nullable=True)
    system_id = db.Column(db.BigInteger)
    system_name = db.Column(db.String(255), nullable=True)
    create_id = db.Column(db.BigInteger)
    db_number = db.Column(db.BigInteger)
    storage_capacity = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
class DbPushField(db.Model):
    __tablename__ = 'db_push_field'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_id = db.Column(db.Integer, nullable=False)
    field_name = db.Column(db.String(255), nullable=False)
    field_type = db.Column(db.String(255), nullable=False)
    field_comment = db.Column(db.String(255))
    is_primary_key = db.Column(db.Boolean, nullable=False, default=False)
    is_nullable = db.Column(db.Boolean, nullable=False, default=False)
    default = db.Column(db.String(255))
    is_autoincrement = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)