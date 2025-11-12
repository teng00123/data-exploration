from backend.config import db
from backend.database.base import BaseModel
from sqlalchemy import Enum

class RuleGroup(BaseModel):
    __table_name__ = 'rule_group'

    group_name = db.Column(db.String(255),comment='规则组名称')
    parent_id = db.Column(db.BigInteger,comment='父级规则组id')


class Rule(BaseModel):
    __table_name = 'rule'

    rule_code = db.Column(db.String(255))
    group_id = db.Column(db.BigInteger)
    business_rules = db.Column(db.String(255))
    database_type = db.Column(db.String(255))
    expression = db.Column(Enum('sql规则配置','正则表达式',name='expression'))
    sql_expression = db.Column(db.TEXT)
    re_expression = db.Column(db.TEXT)
    describe = db.Column(db.String(255))
    refer_text = db.Column(db.Text)
    question_level = db.Column(Enum('轻度','中度','严重',name='question_level'))
    weight = db.Column(db.Integer)
    is_active = db.Column(db.Boolean,default=False)
    rule_version = db.Column(db.Integer)
    rule_type = db.Column(db.String(255))
    up_cycle = db.Column(db.String(255))
    dimension = db.Column(db.String(255))
    is_timeliness = db.Column(db.Boolean,default=False)

class ConfigureRuleInfo(BaseModel):
    __table_name__ = 'configure_rule_info'

    rule_id = db.Column(db.BigInteger)
    field_id = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger)

class ConfigureTimelinessInfo(BaseModel):
    __table_name__ = 'configure_timeliness_info'

    table_id = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger)
    up_cycle = db.Column(db.String(255))

class ConfigureRuleFieldInfo(BaseModel):
    __table_name__ = 'configure_rule_field_info'

    rule_id = db.Column(db.BigInteger)
    field_id1 = db.Column(db.BigInteger)
    field_id2 = db.Column(db.BigInteger)
    table_id = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger)

class ConfigureRuleTableInfo(BaseModel):
    __table_name__ = 'configure_rule_table_info'

    rule_id = db.Column(db.BigInteger)
    field_id1 = db.Column(db.BigInteger)
    field_id2 = db.Column(db.BigInteger)
    table_id1 = db.Column(db.BigInteger)
    table_id2 = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger)

class RuleGroupGraph:

    @staticmethod
    def get_query():
        main_group_infos = RuleGroup.query.filter(RuleGroup.parent_id.is_(None)).all()
        result = []
        for main_group_info in main_group_infos:
            main_group = {
                'group_name':main_group_info.group_name,
                'parent_id':main_group_info.parent_id,
                'id':main_group_info.id,
                # 'count':
                'group':[]
            }
            group_info = RuleGroup.query.filter_by(parent_id=main_group_info.id).all()
            for i in group_info:
                main_group['group'].append({
                'group_name':i.group_name,
                'parent_id':i.parent_id,
                'id':i.id
                # 'count':
                })
            result.append(main_group)
        return result

class RuleGraph:

    @staticmethod
    def get_query_by_group_id(group_id,dimension):
        group_ids = [i.id for i in RuleGroup.query.filter_by(parent_id=group_id).all()]
        group_ids.append(group_id)
        result = Rule.query.filter(Rule.group_id.in_(group_ids)).all()
        if dimension:
            result = Rule.query.filter_by(dimension=dimension).filter(Rule.group_id.in_(group_ids)).all()
        return [{k: v for k, v in i.__dict__.items() if k != '_sa_instance_state'} for i in result]
