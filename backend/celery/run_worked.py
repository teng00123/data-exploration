# run_worker.py

from tasks import celery_app # 导入 tasks.py 中定义的 Celery 应用实例

if __name__ == '__main__':
    # 启动 Celery Worker
    # -l info: 设置日志级别为 info
    # -A app: 指定 Celery 应用实例的模块名 (这里是 tasks.py 中的 app)
    # --loglevel=info: 另一种设置日志级别的方式
    # --pool=gevent: (可选) 使用 gevent 池来提高并发性能 (需要安装 gevent)
    #                 默认是 prefork，每个 worker 是一个进程。
    # --concurrency=4: (可选) 设置并发 worker 数量 (默认是 CPU 核心数)
    celery_app.worker_main(argv=['worker', '-l', 'info', '--loglevel=info', '--pool=gevent', '--concurrency=4']) # 使用 solo 池更简单，不需要额外依赖
    # 如果使用 gevent: app.worker_main(argv=['worker', '-l', 'info', '--loglevel=info', '--pool=gevent', '--concurrency=4'])
