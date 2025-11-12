from backend.config import db
from backend.database.base import BaseModel
import datetime

class Backup(BaseModel):
    __tablename__ = 'backups'

    datasource_id = db.Column(db.BigInteger, nullable=False, comment='数据源ID')
    backup_name = db.Column(db.String(255), nullable=False, comment='备份名称')
    backup_size = db.Column(db.Float, nullable=False, comment='备份大小')
    backup_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, comment='备份时间')
    backup_status = db.Column(db.String(50), nullable=False, comment='备份状态')
    backup_path = db.Column(db.String(255), nullable=False, comment='备份路径')
    backup_type = db.Column(db.String(50), nullable=False, comment='备份类型')
    backup_comment = db.Column(db.String(255), nullable=True, comment='备份备注')
    backup_file = db.Column(db.String(255), nullable=False, comment='备份文件名')
    backup_file_size = db.Column(db.Float, nullable=False, comment='备份文件大小')
    backup_file_path = db.Column(db.String(255), nullable=False, comment='备份文件路径')
    backup_scheduler = db.Column(db.String(255), nullable=True, comment='备份调度器')
