from sqlalchemy import create_engine,text,func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from backend.config import config
from backend.database.schedule_info import ScheduleInfo
from backend.database.sys_model import SysDept
import uuid
import urllib.parse
from datetime import datetime

def run_quality_inspection(data):
    sys_engine = create_engine(
        f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    session = sessionmaker(bind=sys_engine)()
    no_dept_ids = [4, 1851507096929443842, 1861578281075449858, 1856162650240790529]
    sys_dept_ids = [i.dept_id for i in session.query(SysDept).filter_by(parent_id=1,del_flag='0').filter(SysDept.dept_id.not_in(no_dept_ids)).all()]
    dept_ips = [i.department_id for i in session.query(ScheduleInfo).filter(ScheduleInfo.department_id != 4).with_entities(
        ScheduleInfo.department_id,
        func.count(ScheduleInfo.id).label('count')
    ).group_by(ScheduleInfo.department_id).all()]
    dept_ip = set()
    for i in dept_ips:
        dept = session.query(SysDept).filter_by(dept_id=i).first()
        if dept.parent_id == 1:
            dept_ip.add(i)
        else:
            dept_ip.add(dept.parent_id)
    for i in sys_dept_ids:
        # print(i)
        if i not in dept_ip:
            dept_name = session.query(SysDept).filter_by(dept_id=i).first().dept_name
            print(dept_name)
    for i in dept_ip:
        if i not in sys_dept_ids:
            print(i)
    print(len(sys_dept_ids))
    print(len(dept_ip))

# 1906600267833360386
if __name__ == '__main__':
    run_quality_inspection({'id': 1,'scheduler_id': '1'})