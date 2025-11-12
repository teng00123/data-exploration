from backend.config import db
from backend.database.base import BaseModel


class VariableManageInfo(BaseModel):
    __tablename__ = 'variable_manage_info'

    variable_name = db.Column(db.String(255), nullable=False, comment='变量名称')
    variable_cname = db.Column(db.String(255), nullable=False, comment='变量中文名称')
    variable_value = db.Column(db.String(255), nullable=False,unique=True, comment='变量值')
    variable_desc = db.Column(db.String(255), nullable=True, comment='变量描述')