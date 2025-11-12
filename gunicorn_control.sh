#!/bin/bash

# 应用名称（替换为你的应用名称）
APP_NAME="app"
# WSGI 应用模块（替换为你的 WSGI 应用模块）
WSGI_MODULE="app:app"
# Gunicorn 进程 ID 文件
PIDFILE="gunicorn.pid"
# 设置环境变量
export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH

# 启动 Gunicorn
start_gunicorn() {
    echo "Starting Gunicorn..."
    gunicorn -w 4 -b 0.0.0.0:5000 --timeout 1200 --access-logfile access.log --error-logfile error.log $WSGI_MODULE --pid $PIDFILE -D
    echo "Gunicorn started."
}

# 停止 Gunicorn
stop_gunicorn() {
    if [ -f $PIDFILE ]; then
        echo "Stopping Gunicorn..."
        kill -QUIT $(cat $PIDFILE)
        rm -f $PIDFILE
        echo "Gunicorn stopped."
    else
        echo "No Gunicorn process found."
    fi
}

# 检查命令参数
case "$1" in
    start)
        start_gunicorn
        ;;
    stop)
        stop_gunicorn
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

exit 0

