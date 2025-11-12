import copy
import json
from datetime import datetime

from flask import Blueprint,request,jsonify
from backend.database.quality_inspection import QualityInfo,QualitySchedulerInfo,QualityResult
from backend.config import r,db
from scheduler_redis.quality_inspection_utils import run_quality_inspection


quality_inspection_bp = Blueprint('quality_inspection', __name__)


@quality_inspection_bp.route('/query', methods=['POST'])
def query_quality_inspection():
    data = request.get_json()
    page = data.get('page')
    per_page = data.get('per_page')
    # Save data to database
    rule_query = QualityInfo.query
    count = rule_query.count()
    rule_infos = rule_query.paginate(page=page, per_page=per_page).items
    rule_info_list = [i.__dict__ for i in rule_infos]
    rule_info_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                               rule_info_list]
    # Add quality inspection logic here
    return jsonify({'message': 'successfully','code':200,'data':rule_info_list,'count':count})

@quality_inspection_bp.route('/scheduler/query', methods=['POST'])
def scheduler_query_inspection():
    data = request.get_json()
    page = data.get('page')
    per_page = data.get('per_page')
    rule_query = QualitySchedulerInfo.query.order_by(QualitySchedulerInfo.execution_time.desc())
    count = rule_query.count()
    rule_infos = rule_query.paginate(page=page, per_page=per_page).items
    rule_info_list = [i.__dict__ for i in rule_infos]
    rule_info_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                               rule_info_list]
    return jsonify({'message': 'successfully','code':200,'data':rule_info_list,'count':count})

@quality_inspection_bp.route('/details', methods=['POST'])
def quality_inspection_details():
    data = request.get_json()
    id = data.get('id')
    page = data.get('page')
    per_page = data.get('per_page')
    rule_info = QualitySchedulerInfo.query.filter_by(id=id).first()
    quality_query = QualityResult.query.filter_by(scheduler_id=rule_info.scheduler_id)
    count = quality_query.count()
    quality_details = quality_query.paginate(page=page, per_page=per_page).items
    rule_info_list = [i.__dict__ for i in quality_details]
    rule_info_list = [{k: v for k, v in info.items() if k != '_sa_instance_state'} for info in
                               rule_info_list]
    return jsonify({'message': 'successfully','code':200,'data':rule_info_list,'count':count})

@quality_inspection_bp.route('/start', methods=['POST'])
def quality_inspection_start():
    data = request.get_json()
    id = data.get('id')
    type = data.get('conditions')
    cycle = data.get('cycle')
    minute = data.get('minute',None)
    hour = data.get('hour',None)
    day = data.get('day',None)
    week = data.get('week',None)
    rule_info = QualityInfo.query.filter_by(id=id).first()
    rule_info.type = type
    rule_info.cycle = cycle
    rule_info.minute = minute
    rule_info.hour = hour
    rule_info.day = day
    rule_info.week = week
    db.session.commit()
    print(type)
    if type == '立即执行':
        run_quality_inspection(data)
    else:
        data['schedule_type'] = 'quality_time'
        deep_data = copy.deepcopy(data)
        r.publish('scheduler', json.dumps(deep_data))
    return jsonify({'message': 'successfully','code':200})