import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.schedule_info import ScheduleInfo
from backend.database.exploration_model import DatasourceInfo
from backend.config import config, scheduler
from scheduler_redis.uitls import _data_exploration
from scheduler_redis.result_uitls import result_data_exploration
from concurrent.futures import ThreadPoolExecutor
import logging
from logging.handlers import TimedRotatingFileHandler

# 创建一个日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个 TimedRotatingFileHandler
handler = TimedRotatingFileHandler('my_log.log', when='D', interval=1, backupCount=7)
# 'D' 表示每天更新一次，interval=1 表示每 1 天更新一次，backupCount=7 表示保留 7 个旧的日志文件

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(handler)


import json
class Scheduler:
    def __init__(self):
        self.r = redis.Redis(host=config.get('redis').get('host'), port=6379, db=0, password=config.get('redis').get('password'))
        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe('scheduler')

        self.engine = create_engine(f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
        self.session = sessionmaker(bind=self.engine)()

        self.scheduler = scheduler
        self.scheduler.start()

        self.thread_pool = ThreadPoolExecutor(max_workers=config.get('thread'))

    def run(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'].decode())
                    logger.info(data)
                    schedule_info = self.session.query(ScheduleInfo).filter_by(id=data.get('schedule_id')).first()
                    if schedule_info:
                        datasource_info = self.session.query(DatasourceInfo).filter_by(id=schedule_info.datasource_id).first()
                    if data.get('schedule_type') == 'time':
                        if datasource_info.status == '1':
                            if schedule_info.method == 'day':
                                scheduler.add_job(func=_data_exploration, trigger='cron', id=str(schedule_info.id),
                                                  name=schedule_info.name, args=[data],
                                                  hour=schedule_info.hour,
                                                  minute=schedule_info.minute)
                            if schedule_info.method == 'week':
                                scheduler.add_job(func=_data_exploration, trigger='cron', id=str(schedule_info.id),
                                                  name=schedule_info.name, args=[data],
                                                  hour=schedule_info.hour,
                                                  minute=schedule_info.minute, day_of_week=schedule_info.week)
                            if schedule_info.method == 'month':
                                scheduler.add_job(func=_data_exploration, trigger='cron', id=str(schedule_info.id),
                                                  name=schedule_info.name, args=[data],
                                                  hour=schedule_info.hour,
                                                  minute=schedule_info.minute, day=schedule_info.day)
                            logger.info(f"{schedule_info.schedule_name} add schedule sussess")
                        elif datasource_info.status == '2':
                            if schedule_info.method == 'day':
                                scheduler.add_job(func=result_data_exploration, trigger='cron', id=str(schedule_info.id),
                                                  name=schedule_info.name, args=[data],
                                                  hour=schedule_info.hour,
                                                  minute=schedule_info.minute)
                            if schedule_info.method == 'week':
                                scheduler.add_job(func=result_data_exploration, trigger='cron', id=str(schedule_info.id),
                                                  name=schedule_info.name, args=[data],
                                                  hour=schedule_info.hour,
                                                  minute=schedule_info.minute, day_of_week=schedule_info.week)
                            if schedule_info.method == 'month':
                                scheduler.add_job(func=result_data_exploration, trigger='cron', id=str(schedule_info.id),
                                                  name=schedule_info.name, args=[data],
                                                  hour=schedule_info.hour,
                                                  minute=schedule_info.minute, day=schedule_info.day)
                            logger.info(f"{schedule_info.schedule_name} add schedule result table sussess")
                    elif data.get('schedule_type') == 'immediately':
                        if datasource_info.status == '1':
                            self.thread_pool.submit(_data_exploration, data)
                            logger.info(f"{schedule_info.schedule_name} execute sussess")
                        elif datasource_info.status == '2':
                            self.thread_pool.submit(result_data_exploration, data)
                            logger.info(f"{schedule_info.schedule_name} execute result table sussess")
                    elif data.get('schedule_type') == 'delete':
                        scheduler.remove_job(str(data.get('id')))
                        logger.info(f"{data.get('id')} delete sussess")
                except Exception as e:
                    logger.error(str(e))

if __name__ == '__main__':
    Scheduler().run()