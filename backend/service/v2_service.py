from backend.database.schedule_info import ScheduleExecute
from backend.database.exploration_model import TableInfo,FieldInfo
from backend.database.rule import Rule
from backend.config import db


class V2_Service:

    @staticmethod
    def get_data_scanning_status() -> dict:
        result = {}
        result['datasource_count'] = db.session.query(ScheduleExecute.datasource_id).group_by(
            ScheduleExecute.datasource_id).count()
        result['table_count'] = db.session.query(TableInfo.table_name, TableInfo.datasource_id).group_by(
            TableInfo.table_name, TableInfo.datasource_id).count()
        result['field_count'] = db.session.query(FieldInfo.name, FieldInfo.table_info_id).group_by(
            FieldInfo.name, FieldInfo.table_info_id).count()
        result['rule_count'] = db.session.query(Rule).count()
        return result

    @staticmethod
    def get_scaning_progress() -> dict:
        result = {}
        result['success_count'] = db.session.query(ScheduleExecute).filter(ScheduleExecute.schedule_status == '成功').count()
        result['fail_count'] = db.session.query(ScheduleExecute).filter(ScheduleExecute.schedule_status == '失败').count()
        result['execute_count'] = db.session.query(ScheduleExecute).filter(ScheduleExecute.schedule_status == '执行中').count()
        return result