from celery import Celery
from tasks import redis_url

if __name__ == '__main__':
    app = Celery("distributed_task_demo", broker=f'{redis_url}/0')
    print(app)

    # for i in range(1,10):
    app.send_task("tasks.empty_value_detection", args=(1, 4, 1, 'biz_data_directory', 'table_id,system_name'))
