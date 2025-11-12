
from tasks import celery_app # 导入 tasks.py 中定义的 Celery 应用实例
from celery.bin import beat
if __name__ == '__main__':

    celery_app.start(argv=['beat', '-l', 'info', '--loglevel=info','-S','celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler'])