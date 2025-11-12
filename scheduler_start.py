from scheduler_redis.scheduler import Scheduler
# from scheduler_redis.scheduler_quality import Scheduler as Scheduler_quality
# import threading

if __name__ == '__main__':
    # t1 = threading.Thread(target=Scheduler().run)
    # t2 = threading.Thread(target=Scheduler_quality().run)
    # t1.start()
    # t2.start()
    Scheduler().run()