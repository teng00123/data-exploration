from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from backend.config import config
from backend.database.quality_inspection import QualityResult,QualitySchedulerInfo,QualityInfo
from backend.database.directory import DataDirectory,DataDirectoryItem
from backend.database.sys_model import SysDept
import uuid
import urllib.parse
from datetime import datetime

def run_quality_inspection(data):
    sys_engine = create_engine(
        f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    session = sessionmaker(bind=sys_engine)()
    quality_info = session.query(QualityInfo).filter_by(id=data.get('id')).first()
    scheduler_id = str(uuid.uuid4())
    execution_time = datetime.timestamp(datetime.now())
    quality_scheduer_info = QualitySchedulerInfo(
        quality_name=quality_info.quality_name,
        execution_time=execution_time,
        scheduler_id=scheduler_id
    )
    quality_info.execution_time = execution_time
    session.add(quality_scheduer_info)
    session.flush()
    rule_info = session.query(SysDept).filter_by(parent_id=1,del_flag='0').filter(SysDept.dept_id != 4).all()
    for rule in rule_info:
        dept_name = rule.dept_name
        data_directory_none = session.query(DataDirectory).filter(DataDirectory.parent_dept_id==rule.dept_id).filter(
            or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.cn_name.is_(None)).filter(DataDirectory.build_directory.is_(True)).count()
        data_directory_datazie_none = session.query(DataDirectory).filter(DataDirectory.parent_dept_id==rule.dept_id).filter(
            or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.data_zie.is_(None)).filter(DataDirectory.build_directory.is_(True)).count()
        data_directory_datastorge_none = session.query(DataDirectory).filter(
            DataDirectory.parent_dept_id==rule.dept_id).filter(
            or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(
            DataDirectory.data_storage_capacity.is_(None)).filter(DataDirectory.build_directory.is_(True)).count()
        data_directory_item_none_total = session.query(DataDirectoryItem).filter(
            DataDirectoryItem.item_name.is_(None)).join(DataDirectory,DataDirectoryItem.data_directory_id==DataDirectory.id).filter(DataDirectory.parent_dept_id==rule.dept_id).filter(
            or_(DataDirectory.status == '2', DataDirectory.status == '3')).filter(DataDirectory.build_directory.is_(True)).count()
        quality_result = QualityResult(
            scheduler_id = scheduler_id,
            dept_name=dept_name,
            data_none_total=data_directory_none,
            datazie_total=data_directory_datazie_none,
            datastorage_total=data_directory_datastorge_none,
            field_none_total=data_directory_item_none_total
        )
        session.add(quality_result)
        session.flush()
    session.commit()



if __name__ == '__main__':
    run_quality_inspection({'id': 1,'scheduler_id': '1'})