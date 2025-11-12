#!/bin/bash

# Python 脚本的名称
PYTHON_SCRIPT="scheduler_start.py"
# Python 脚本的进程 ID 文件
PIDFILE="scheduler_start.pid"

# 启动 Python 脚本
start() {
    echo "Starting Python script..."
    nohup python $PYTHON_SCRIPT > /dev/null 2>&1 &
    echo $! > $PIDFILE
    echo "Python script started."
}

# 停止 Python 脚本
stop() {
    if [ -f $PIDFILE ]; then
        echo "Stopping Python script..."
        kill -9 $(cat $PIDFILE)
        rm -f $PIDFILE
        echo "Python script stopped."
    else
        echo "No Python script process found."
    fi
}

# 检查命令参数
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

exit 0
