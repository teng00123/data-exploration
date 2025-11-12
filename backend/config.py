import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_sqlalchemy import SQLAlchemy
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os
import redis
import urllib.parse


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def read_config(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config


config = read_config(BASE_DIR + '/config.yaml')
db = SQLAlchemy()

scheduler = BackgroundScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url=f'postgresql://{config["database"]["user"]}:{urllib.parse.quote_plus(config["database"]["password"])}@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user')
    }, executors={
        'default': ThreadPoolExecutor(config['scheduler']['thread_num']),
        'processpool': ProcessPoolExecutor(config['scheduler']['process_num'])
    },
    job_defaults={
        'coalesce': False,
        'misfire_grace_time':None,
        'max_instances': config['scheduler']['max_instances']
    }
)

r = redis.Redis(host=config.get('redis').get('host'), port=6379, db=0, password=config.get('redis').get('password'))