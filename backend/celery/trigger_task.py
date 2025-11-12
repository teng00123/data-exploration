# trigger_task.py

from tasks import simulate_long_running_task,empty_value_detection,repetitive_detection,timeliness_detection # 从 tasks.py 导入任务函数

if __name__ == '__main__':
    print("Triggering a distributed task...")
    # 异步调用任务
    # .delay() 是最简单的异步调用方式
    # 可以传递参数给任务函数
    # task = simulate_long_running_task.delay(message="Hello from Trigger!")
    #
    # print(f"Task triggered! Task ID: {task.id}")

    # (可选) 等待任务完成并获取结果
    # 注意: 这会阻塞当前线程，直到任务完成。
    # 在 Web 请求中通常不这样做，而是返回任务 ID 让客户端稍后查询。
    print("Waiting for task to complete...")
    # result = task.get(timeout=30) # 等待最多 30 秒
    # print(f"Task result: {result}")

    # empty_task = empty_value_detection.delay(execute_id=1,database_id=4,rule_id=1,table_name='biz_data_directory',field_name='table_id,system_name')
    # repetitive_task = repetitive_detection.delay(database_id=4,rule_id=3,table_name='biz_data_directory',field_name='table_id,system_name')
    # timeliness_task = timeliness_detection.delay(database_id=45,rule_id=3,table_name='quality_integrity',field_name='updated_at',update_type='year')
    # print(f"Empty Task triggered! Task ID: {empty_task.id}")
    print(f"Empty Task triggered! Task ID: {timeliness_task.id}")

    # (可选) 检查任务状态
    # print(f"Task status: {task.state}")
    # if task.ready():
    #     print(f"Task result: {task.result}")
    #     if task.failed():
    #         print(f"Task failed! Exception: {task.result}")
