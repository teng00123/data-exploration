# 数据探查平台 (Data Exploration Platform)

> 📖 [English Documentation](#english-documentation) | 中文文档见下方

---

## 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
  - [环境要求](#环境要求)
  - [配置文件](#配置文件)
  - [环境变量（安全配置）](#环境变量安全配置)
  - [启动程序](#启动程序)
- [离线环境部署](#离线环境部署)
  - [Docker 安装](#docker-安装)
  - [离线安装中间件镜像](#离线安装中间件镜像)
  - [离线安装 JDK](#离线安装-jdk)
- [定时任务模块](#定时任务模块)
- [Oracle 配置](#oracle-配置)
- [开发指南](#开发指南)

---

## 项目简介

数据探查平台是一个面向企业的**数据质量检测与管理系统**，提供以下核心能力：

- 📊 **数据质量检测**：完整性、唯一性（重复性）、准确性、一致性多维度检测
- ⏰ **及时性检查**：配置数据更新周期，自动检测数据是否按时更新
- 📋 **规范性检查**：检测表/字段是否缺少注释、是否缺少主键等规范问题
- 📅 **定时任务调度**：基于 Celery + Redis 的异步任务队列，支持 Cron 表达式调度
- 📄 **报告生成**：自动生成 PDF 质量检测报告，支持 AI 辅助分析
- 🔗 **多数据源接入**：支持 PostgreSQL、MySQL、Oracle、DM（达梦）、SQLite

---

## 技术栈

| 组件 | 版本 |
|------|------|
| Python | 3.8+ |
| Flask | 3.0.3 |
| SQLAlchemy | 2.0.36 |
| Celery | 5.4.0 |
| APScheduler | 3.10.4 |
| Redis | 6.x |
| PostgreSQL | 16.x |

---

## 项目结构

```
data-exploration/
├── app.py                      # Flask 应用入口
├── init_nacos_database.py      # 数据库初始化脚本
├── requirements.txt            # Python 依赖
├── gunicorn_control.sh         # Gunicorn 启动/停止脚本
├── scheduler_control.sh        # 定时任务启动脚本
├── scheduler_quality_start.py  # 质量检测调度器入口
├── backend/
│   ├── config.py               # 应用配置（DB、Redis、Scheduler）
│   ├── config.yaml             # 配置文件（数据库、Redis、调度参数）
│   ├── utils.py                # 工具函数（加解密、分页、装饰器等）
│   ├── database/               # SQLAlchemy 数据模型
│   ├── routers/                # Flask Blueprint 路由
│   │   ├── v1.py               # 规则管理、数据源、调度、报告接口
│   │   ├── v2.py               # 数据探查接口 v2
│   │   ├── v3.py               # 数据探查接口 v3
│   │   ├── v4.py               # 数据探查接口 v4
│   │   ├── exploration.py      # 数据探查核心接口
│   │   ├── quality_inspection.py # 质量检测接口
│   │   ├── auth.py             # 认证接口
│   │   ├── management.py       # 管理接口
│   │   └── ...
│   ├── service/                # 业务逻辑层
│   ├── celery/                 # Celery 异步任务
│   ├── llm/                    # 大模型集成（OpenAI）
│   ├── expand/                 # 数据预处理扩展
│   ├── template/               # 报告模板
│   ├── response/               # 统一响应格式
│   └── sql/                    # 数据库初始化 SQL
├── scheduler_redis/            # Redis 调度器模块
└── data_resources/             # 数据资源文件
```

---

## 快速开始

### 环境要求

- Python 3.8+
- PostgreSQL 16+
- Redis 6+
- （可选）Oracle Instant Client（接入 Oracle 数据源时需要）

### 配置文件

复制并编辑 `backend/config.yaml`：

```yaml
# 数据库配置（PostgreSQL，用于存储平台自身数据）
database:
  host: 127.0.0.1
  port: 5432
  user: postgres
  password: your_password

# Redis 配置
redis:
  host: 127.0.0.1
  port: 6379
  password: your_redis_password   # 无密码则留空或删除此项

# 定时任务配置
scheduler:
  thread_num: 20    # 线程池大小
  process_num: 5    # 进程池大小
  max_instances: 3  # 单任务最大并发实例数

# 报告文件存储路径
report_file: /data/reports/

# 上传文件存储路径
UPLOAD_FOLDER: /data/uploads/
```

### 环境变量（安全配置）

生产环境务必通过环境变量设置以下敏感配置，**不要将密钥硬编码或提交到代码仓库**：

```bash
# JWT 签名密钥（必填，建议使用随机生成的强密钥）
export JWT_SECRET_KEY="your-strong-random-jwt-secret"

# Fernet 加密密钥（用于密码加解密，必填）
# 生成方式：python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
export FERNET_KEY="your-fernet-key"
```

### 安装依赖

```bash
# 在线安装
pip install -r requirements.txt

# 离线安装（使用预打包的离线包）
mkdir venv_offline
tar -zxvf data-exploration.tar.gz -C venv_offline
source venv_offline/bin/activate
```

### 初始化数据库

```bash
# 首次部署时执行，创建所有数据表
python init_nacos_database.py
```

### 启动程序

```bash
# 启动 Web 服务（Gunicorn）
./gunicorn_control.sh start

# 停止 Web 服务
./gunicorn_control.sh stop

# 查看错误日志
tail -f error.log

# 启动定时任务调度器
./scheduler_control.sh start

# 启动质量检测调度器
./scheduler_quality_start.sh
```

开发模式直接运行：

```bash
python app.py
# 默认监听 0.0.0.0:5000
```

---

## 离线环境部署

### Docker 安装

```bash
# 解压 Docker 二进制包
tar -zxvf docker-20.10.0.tgz
cp docker/* /usr/bin/

# 创建 systemd 服务文件
vi /usr/lib/systemd/system/docker.service
```

将以下内容写入 `docker.service`：

```ini
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
```

```bash
# 启动 Docker
systemctl daemon-reload
systemctl enable docker
systemctl start docker

# 验证安装
docker info
```

### 离线安装中间件镜像

```bash
# PostgreSQL 16
docker load -i postgre16.tar
bash postgres_docker_run.sh

# Redis 6
docker load -i redis-6.0.8.tar
bash redis6.0.8_run.sh

# Nginx（可选）
docker load -i nginx.tar
```

### 离线安装 JDK

```bash
# 解压 JDK
tar -zxvf jdk-8u171-linux-x64.tar.gz

# 配置环境变量（追加到 /etc/profile）
cat >> /etc/profile << 'EOF'
export JAVA_HOME=/opt/jdk1.8.0_171
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
EOF

source /etc/profile
java -version
```

---

## 定时任务模块

平台使用两套调度机制：

| 模块 | 说明 |
|------|------|
| `scheduler_redis/` | 基于 Redis Pub/Sub 的调度器，监听调度事件动态增删任务 |
| `backend/celery/` | 基于 Celery 的异步任务队列，执行实际的质量检测任务 |

```bash
# 启动 Celery Worker
cd backend/celery
python run_worked.py

# 启动 Celery Beat（定时触发）
python run_beat.py
```

---

## Oracle 配置

接入 Oracle 数据源时，需安装 Oracle Instant Client 并配置动态链接库路径：

```bash
export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH

# 建议写入 /etc/profile 或 ~/.bashrc 使其永久生效
echo 'export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 开发指南

### API 路由说明

| 前缀 | 模块 | 说明 |
|------|------|------|
| `/v1` | routers/v1.py | 规则管理、数据源查询、调度管理、质量报告 |
| `/v2` | routers/v2.py | 数据探查 v2 接口 |
| `/v3` | routers/v3.py | 数据探查 v3 接口 |
| `/v4` | routers/v4.py | 数据探查 v4 接口 |
| `/exploration` | routers/exploration.py | 数据探查核心接口 |
| `/quality_inspection` | routers/quality_inspection.py | 质量检测配置接口 |
| `/oauth` | routers/auth.py | 用户认证（JWT） |
| `/api-auth/v1/oauth` | routers/oauth.py | OAuth 认证 |
| `/report` | routers/report_forms.py | 报表接口 |
| `/mange` | routers/management.py | 管理接口 |

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/teng00123/data-exploration.git
cd data-exploration

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export JWT_SECRET_KEY="dev-secret-key"
export FERNET_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"

# 配置 config.yaml 后启动
python app.py
```

---

---

# English Documentation

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [Offline Deployment](#offline-deployment)
- [Scheduler Modules](#scheduler-modules)
- [Oracle Support](#oracle-support)
- [Development Guide](#development-guide)

---

## Overview

**Data Exploration Platform** is an enterprise-grade **data quality inspection and management system** providing:

- 📊 **Multi-dimensional Quality Checks** — completeness, uniqueness, accuracy, consistency
- ⏰ **Timeliness Inspection** — configure update cycles and automatically detect stale data
- 📋 **Schema Compliance Checks** — missing comments, missing primary keys, and other standards
- 📅 **Scheduled Task Management** — Celery + Redis async queue with Cron expression support
- 📄 **Report Generation** — auto-generate PDF quality reports with optional AI-assisted analysis
- 🔗 **Multi-datasource Support** — PostgreSQL, MySQL, Oracle, DM (Dameng), SQLite

---

## Tech Stack

| Component | Version |
|-----------|---------|
| Python | 3.8+ |
| Flask | 3.0.3 |
| SQLAlchemy | 2.0.36 |
| Celery | 5.4.0 |
| APScheduler | 3.10.4 |
| Redis | 6.x |
| PostgreSQL | 16.x |

---

## Project Structure

```
data-exploration/
├── app.py                      # Flask application entry point
├── init_nacos_database.py      # Database initialization script
├── requirements.txt            # Python dependencies
├── gunicorn_control.sh         # Gunicorn start/stop script
├── scheduler_control.sh        # Scheduler start script
├── scheduler_quality_start.py  # Quality scheduler entry point
├── backend/
│   ├── config.py               # App config (DB, Redis, Scheduler)
│   ├── config.yaml             # Configuration file
│   ├── utils.py                # Utilities (crypto, pagination, decorators)
│   ├── database/               # SQLAlchemy models
│   ├── routers/                # Flask Blueprint routes
│   │   ├── v1.py               # Rules, datasource, schedule, report APIs
│   │   ├── v2.py ~ v4.py       # Exploration APIs v2–v4
│   │   ├── exploration.py      # Core exploration APIs
│   │   ├── quality_inspection.py
│   │   ├── auth.py             # JWT authentication
│   │   └── ...
│   ├── service/                # Business logic layer
│   ├── celery/                 # Celery async tasks
│   ├── llm/                    # LLM integration (OpenAI)
│   ├── expand/                 # Data preprocessing extensions
│   ├── template/               # Report templates
│   ├── response/               # Unified response format
│   └── sql/                    # Database init SQL files
├── scheduler_redis/            # Redis pub/sub scheduler module
└── data_resources/             # Data resource files
```

---

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 16+
- Redis 6+
- (Optional) Oracle Instant Client — required for Oracle datasource support

### Configuration

Copy and edit `backend/config.yaml`:

```yaml
# PostgreSQL — used for platform's own data storage
database:
  host: 127.0.0.1
  port: 5432
  user: postgres
  password: your_password

# Redis
redis:
  host: 127.0.0.1
  port: 6379
  password: your_redis_password   # leave empty if no password

# Scheduler settings
scheduler:
  thread_num: 20    # thread pool size
  process_num: 5    # process pool size
  max_instances: 3  # max concurrent instances per job

# Report file storage path
report_file: /data/reports/

# Upload file storage path
UPLOAD_FOLDER: /data/uploads/
```

### Environment Variables

In production, **always** configure sensitive values via environment variables — never commit secrets to version control:

```bash
# JWT signing secret (required — use a strong random string)
export JWT_SECRET_KEY="your-strong-random-jwt-secret"

# Fernet encryption key (required — used for password encryption/decryption)
# Generate one: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
export FERNET_KEY="your-fernet-key"
```

### Install Dependencies

```bash
# Online install
pip install -r requirements.txt

# Offline install (using pre-packaged archive)
mkdir venv_offline
tar -zxvf data-exploration.tar.gz -C venv_offline
source venv_offline/bin/activate
```

### Initialize Database

```bash
# Run once on first deployment to create all tables
python init_nacos_database.py
```

### Running the App

```bash
# Start web service (Gunicorn)
./gunicorn_control.sh start

# Stop web service
./gunicorn_control.sh stop

# View error logs
tail -f error.log

# Start the task scheduler
./scheduler_control.sh start

# Start the quality inspection scheduler
./scheduler_quality_start.sh
```

Development mode:

```bash
python app.py
# Listens on 0.0.0.0:5000 by default
```

---

## Offline Deployment

### Install Docker (Offline)

```bash
# Extract Docker binaries
tar -zxvf docker-20.10.0.tgz
cp docker/* /usr/bin/

# Create systemd service
vi /usr/lib/systemd/system/docker.service
```

Write the following to `docker.service`:

```ini
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable docker
systemctl start docker
docker info
```

### Load Offline Docker Images

```bash
# PostgreSQL 16
docker load -i postgre16.tar
bash postgres_docker_run.sh

# Redis 6
docker load -i redis-6.0.8.tar
bash redis6.0.8_run.sh

# Nginx (optional)
docker load -i nginx.tar
```

### Install JDK Offline

```bash
tar -zxvf jdk-8u171-linux-x64.tar.gz

cat >> /etc/profile << 'EOF'
export JAVA_HOME=/opt/jdk1.8.0_171
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
EOF

source /etc/profile
java -version
```

---

## Scheduler Modules

The platform uses two scheduling mechanisms:

| Module | Description |
|--------|-------------|
| `scheduler_redis/` | Redis Pub/Sub-based scheduler — dynamically adds/removes jobs by listening to events |
| `backend/celery/` | Celery async task queue — executes the actual quality inspection tasks |

```bash
# Start Celery Worker
cd backend/celery
python run_worked.py

# Start Celery Beat (periodic trigger)
python run_beat.py
```

---

## Oracle Support

To connect Oracle datasources, install Oracle Instant Client and configure the library path:

```bash
export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH

# Make it permanent
echo 'export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## Development Guide

### API Route Reference

| Prefix | Module | Description |
|--------|--------|-------------|
| `/v1` | routers/v1.py | Rule management, datasource, scheduling, quality reports |
| `/v2` | routers/v2.py | Exploration APIs v2 |
| `/v3` | routers/v3.py | Exploration APIs v3 |
| `/v4` | routers/v4.py | Exploration APIs v4 |
| `/exploration` | routers/exploration.py | Core exploration APIs |
| `/quality_inspection` | routers/quality_inspection.py | Quality inspection config |
| `/oauth` | routers/auth.py | User authentication (JWT) |
| `/api-auth/v1/oauth` | routers/oauth.py | OAuth authentication |
| `/report` | routers/report_forms.py | Report APIs |
| `/mange` | routers/management.py | Management APIs |

### Local Development Setup

```bash
# Clone the repo
git clone https://github.com/teng00123/data-exploration.git
cd data-exploration

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export JWT_SECRET_KEY="dev-secret-key"
export FERNET_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"

# Edit backend/config.yaml, then start
python app.py
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

*For issues or questions, please open a GitHub Issue.*
