from datetime import datetime
import time
from flask import Flask
# from flask_cors import CORS
from backend.config import scheduler, db, config
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
from logging.handlers import RotatingFileHandler
import os
import re
from flask_jwt_extended import JWTManager
import urllib.parse


def create_tables(app):
    with app.app_context():
        db.create_all()

def before_first_request_func(app):
    from backend.database.schedule_info import ScheduleExecute
    with app.app_context():
        db.create_all()
        schedule_executes = ScheduleExecute.query.filter_by(schedule_status='执行中').all()
        for schedule_execute in schedule_executes:
            schedule_execute.schedule_status = '失败'
            schedule_execute.failure_reason = '程序重启'
            schedule_execute.schedule_time = int(datetime.now().timestamp())
            db.session.commit()


def init_app():
    app = Flask(__name__)

    # create_database('bsp-user',
    #                 f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}:{config["database"]["port"]}/postgres')
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 设置 SQLALCHEMY_POOL_SIZE，定义连接池的大小
    app.config['SQLALCHEMY_POOL_SIZE'] = 10

    # 设置 SQLALCHEMY_MAX_OVERFLOW，定义连接池中可以超过最大数量的连接数
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5

    # 设置 SQLALCHEMY_POOL_TIMEOUT，定义连接池中连接的超时时间
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300

    # 设置 SQLALCHEMY_POOL_RECYCLE，定义连接池中连接的回收时间（秒）
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
    import datetime
    app.config['JWT_SECRET_KEY'] = 'Xi_HpEd93wgZ5G_HCaz1GT11PKalgUQo5aeEXidLkg8='
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=10)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # 设置日志文件路径
    log_file = BASE_DIR + '/error.log'

    # 创建一个日志记录器
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=3)
    handler.setLevel(logging.INFO)

    # 创建一个日志格式器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # 将日志记录器添加到Flask应用中
    app.logger.addHandler(handler)
    jwt = JWTManager(app)
    db.init_app(app)
    # CORS(app)
    from backend.routers import exploration_bp
    from backend.routers import dept_bp
    # from backend.routers import llm_chat_bp
    from backend.routers import report_froms_bp
    from backend.routers import oauth_bp
    from backend.routers import auth_bp
    from backend.routers import db_push_bp
    from backend.routers import quality_inspection_bp
    from backend.routers import large_bp
    from backend.routers import v1_router
    from backend.routers import v2_router
    from backend.routers import v3_router
    from backend.routers import v4_router
    from backend.routers import mange_router

    app.register_blueprint(exploration_bp, url_prefix='/exploration')
    app.register_blueprint(dept_bp, url_prefix='/dept')
    # app.register_blueprint(llm_chat_bp, url_prefix='/ai')
    app.register_blueprint(report_froms_bp, url_prefix='/report')
    app.register_blueprint(auth_bp, url_prefix='/oauth')
    app.register_blueprint(oauth_bp, url_prefix='/api-auth/v1/oauth')
    app.register_blueprint(db_push_bp, url_prefix='/api-user/v1/db/push')
    app.register_blueprint(quality_inspection_bp, url_prefix='/quality_inspection')
    app.register_blueprint(large_bp, url_prefix='/large')
    app.register_blueprint(v1_router, url_prefix='/v1')
    app.register_blueprint(v2_router, url_prefix='/v2')
    app.register_blueprint(v3_router, url_prefix='/v3')
    app.register_blueprint(v4_router, url_prefix='/v4')
    app.register_blueprint(mange_router, url_prefix='/mange')
    before_first_request_func(app)
    return app
app = init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

