<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Redis-6.x-DC382D?style=for-the-badge&logo=redis&logoColor=white"/>
<img src="https://img.shields.io/badge/Celery-5.4.0-37814A?style=for-the-badge&logo=celery&logoColor=white"/>

<br/>

# 🔍 数据探查平台
### Data Exploration Platform

**企业级多维数据质量检测与管理系统**

*Enterprise-grade Multi-dimensional Data Quality Inspection & Management System*

<br/>

[![GitHub last commit](https://img.shields.io/github/last-commit/teng00123/data-exploration?style=flat-square)](https://github.com/teng00123/data-exploration/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/teng00123/data-exploration?style=flat-square)](https://github.com/teng00123/data-exploration/issues)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

<br/>

📖 [中文文档](#-中文文档) &nbsp;|&nbsp; [English Docs](#-english-documentation)

</div>

---

## 📋 中文文档

- [✨ 项目简介](#-项目简介)
- [🛠 技术栈](#-技术栈)
- [📁 项目结构](#-项目结构)
- [🚀 快速开始](#-快速开始)
- [🏭 离线环境部署](#-离线环境部署)
- [⚙️ 定时任务模块](#️-定时任务模块)
- [🗄 Oracle 配置](#-oracle-配置)
- [👨‍💻 开发指南](#-开发指南)

---

## ✨ 项目简介

数据探查平台是一个面向企业的 **数据质量检测与管理系统**，提供全链路的数据质量保障能力：

<br/>

|  功能 | 说明 |
|:---:|:---|
| 📊 **多维质量检测** | 完整性、唯一性、准确性、一致性四大维度检测 |
| ⏰ **及时性检查** | 配置数据更新周期，自动检测数据是否按时更新 |
| 📋 **规范性检查** | 检测表/字段是否缺少注释、是否缺少主键等规范问题 |
| 📅 **定时任务调度** | 基于 Celery + Redis 的异步队列，支持 Cron 表达式 |
| 📄 **报告自动生成** | 自动生成 PDF 质量检测报告，支持 AI 辅助分析 |
| 🔗 **多数据源接入** | 支持 PostgreSQL、MySQL、Oracle、DM（达梦）、SQLite |

---

## 🛠 技术栈

<div align="center">

| 组件 | 版本 | 用途 |
|:----:|:----:|:----:|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.8+ | 后端语言 |
| ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) | 3.0.3 | Web 框架 |
| ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) | 2.0.36 | ORM |
| ![Celery](https://img.shields.io/badge/-Celery-37814A?logo=celery&logoColor=white) | 5.4.0 | 异步任务队列 |
| ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white) | 16.x | 主数据库 |
| ![Redis](https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white) | 6.x | 缓存 & 消息队列 |

</div>

---

## 📁 项目结构

```
data-exploration/
│
├── 📄 app.py                      # Flask 应用入口
├── 📄 init_nacos_database.py      # 数据库初始化脚本
├── 📄 requirements.txt            # Python 依赖清单
├── 🔧 gunicorn_control.sh         # Gunicorn 启动/停止脚本
├── 🔧 scheduler_control.sh        # 定时任务启动脚本
├── 🔧 scheduler_quality_start.sh  # 质量检测调度器启动脚本
│
└── 📂 backend/
    ├── ⚙️  config.py               # 应用配置（DB / Redis / Scheduler）
    ├── ⚙️  config.yaml             # 配置文件
    ├── 🛠  utils.py                # 工具函数（加解密、分页、装饰器）
    ├── 📂 database/               # SQLAlchemy 数据模型
    ├── 📂 routers/                # Flask Blueprint 路由层
    │   ├── v1.py                  #   规则、数据源、调度、质量报告
    │   ├── v2.py ~ v4.py          #   数据探查接口 v2–v4
    │   ├── exploration.py         #   数据探查核心接口
    │   ├── quality_inspection.py  #   质量检测配置接口
    │   ├── auth.py                #   JWT 认证
    │   └── ...
    ├── 📂 service/                # 业务逻辑层
    ├── 📂 celery/                 # Celery 异步任务
    ├── 📂 llm/                    # 大模型集成（OpenAI）
    ├── 📂 expand/                 # 数据预处理扩展
    ├── 📂 template/               # 报告模板
    ├── 📂 response/               # 统一响应格式
    └── 📂 sql/                    # 数据库初始化 SQL
```

---

## 🚀 快速开始

### 📌 环境要求

> - **Python** 3.8+
> - **PostgreSQL** 16+
> - **Redis** 6+
> - **Oracle Instant Client**（可选，接入 Oracle 时需要）

### 📝 配置文件

复制并按实际环境编辑 `backend/config.yaml`：

```yaml
# ── 数据库配置（PostgreSQL，存储平台自身数据）──────────────────
database:
  host: 127.0.0.1
  port: 5432
  user: postgres
  password: your_password

# ── Redis 配置 ────────────────────────────────────────────────
redis:
  host: 127.0.0.1
  port: 6379
  password: your_redis_password   # 无密码则删除此行

# ── 定时任务配置 ──────────────────────────────────────────────
scheduler:
  thread_num: 20    # 线程池大小
  process_num: 5    # 进程池大小
  max_instances: 3  # 单任务最大并发实例数

# ── 文件存储路径 ──────────────────────────────────────────────
report_file: /data/reports/
UPLOAD_FOLDER: /data/uploads/
```

### 🔐 环境变量（安全配置）

> ⚠️ **生产环境必须通过环境变量设置密钥，切勿将密钥提交到代码仓库！**

```bash
# JWT 签名密钥
export JWT_SECRET_KEY="your-strong-random-jwt-secret"

# Fernet 加密密钥（用于密码加解密）
# 生成命令：
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

### 📦 安装依赖

```bash
# 在线安装
pip install -r requirements.txt

# 离线安装（使用预打包离线环境）
tar -zxvf data-exploration.tar.gz -C venv_offline
source venv_offline/bin/activate
```

### 🗃 初始化数据库

```bash
# 首次部署时执行，创建所有数据表
python init_nacos_database.py
```

### ▶️ 启动服务

```bash
# 启动 Web 服务（Gunicorn）
./gunicorn_control.sh start

# 停止 Web 服务
./gunicorn_control.sh stop

# 启动定时任务调度器
./scheduler_control.sh start

# 查看实时日志
tail -f error.log
```

**开发模式：**

```bash
python app.py
# 默认监听 http://0.0.0.0:5000
```

---

## 🏭 离线环境部署

### 🐳 Docker 安装

```bash
# 1. 解压 Docker 二进制包
tar -zxvf docker-20.10.0.tgz && cp docker/* /usr/bin/

# 2. 创建 systemd 服务
vi /usr/lib/systemd/system/docker.service
```

<details>
<summary>📋 点击展开 docker.service 配置内容</summary>

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

</details>

```bash
# 3. 启动 Docker
systemctl daemon-reload && systemctl enable docker && systemctl start docker

# 4. 验证安装
docker info
```

### 📦 加载离线镜像

```bash
# PostgreSQL 16
docker load -i postgre16.tar && bash postgres_docker_run.sh

# Redis 6
docker load -i redis-6.0.8.tar && bash redis6.0.8_run.sh

# Nginx（可选）
docker load -i nginx.tar
```

### ☕ 离线安装 JDK

```bash
# 解压并配置环境变量
tar -zxvf jdk-8u171-linux-x64.tar.gz -C /opt/

cat >> /etc/profile << 'EOF'
export JAVA_HOME=/opt/jdk1.8.0_171
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
EOF

source /etc/profile && java -version
```

---

## ⚙️ 定时任务模块

平台使用两套互补的调度机制：

```
┌─────────────────────────────────────────────────────┐
│                   调度架构                           │
│                                                     │
│  HTTP 请求                                           │
│     │                                               │
│     ▼                                               │
│  scheduler_redis/          backend/celery/           │
│  ┌────────────┐            ┌──────────────┐         │
│  │ Redis      │  发布任务  │ Celery Worker│         │
│  │ Pub/Sub    │ ─────────► │ 执行质量检测  │         │
│  │ 动态增删任务│            │              │         │
│  └────────────┘            └──────────────┘         │
└─────────────────────────────────────────────────────┘
```

```bash
# 启动 Celery Worker
cd backend/celery && python run_worked.py

# 启动 Celery Beat（周期性触发）
python run_beat.py
```

---

## 🗄 Oracle 配置

```bash
# 配置 Oracle Instant Client 动态链接库
export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH

# 永久生效
echo 'export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 👨‍💻 开发指南

### 🗺 API 路由总览

| 前缀 | 模块 | 说明 |
|:-----|:-----|:-----|
| `/v1` | routers/v1.py | 规则管理、数据源查询、调度管理、质量报告 |
| `/v2` | routers/v2.py | 数据探查接口 v2 |
| `/v3` | routers/v3.py | 数据探查接口 v3 |
| `/v4` | routers/v4.py | 数据探查接口 v4 |
| `/exploration` | routers/exploration.py | 数据探查核心接口 |
| `/quality_inspection` | routers/quality_inspection.py | 质量检测配置 |
| `/oauth` | routers/auth.py | 用户认证（JWT） |
| `/api-auth/v1/oauth` | routers/oauth.py | OAuth 认证 |
| `/report` | routers/report_forms.py | 报表接口 |
| `/mange` | routers/management.py | 管理接口 |

### 💻 本地开发

```bash
# 1. 克隆仓库
git clone https://github.com/teng00123/data-exploration.git
cd data-exploration

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置环境变量
export JWT_SECRET_KEY="dev-secret-key"
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# 4. 配置 backend/config.yaml 后启动
python app.py
```

### 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交变更：`git commit -m 'feat: 添加新功能'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

---

<br/>

---

<br/>

<div align="center">

# 🔍 English Documentation

**Enterprise-grade Multi-dimensional Data Quality Inspection & Management System**

</div>

---

## 📋 Table of Contents

- [✨ Overview](#-overview)
- [🛠 Tech Stack](#-tech-stack-1)
- [📁 Project Structure](#-project-structure-1)
- [🚀 Quick Start](#-quick-start-1)
- [🏭 Offline Deployment](#-offline-deployment)
- [⚙️ Scheduler Modules](#️-scheduler-modules)
- [🗄 Oracle Support](#-oracle-support)
- [👨‍💻 Development Guide](#-development-guide-1)

---

## ✨ Overview

**Data Exploration Platform** is an enterprise-grade system for **data quality inspection and management**, providing end-to-end data quality assurance:

<br/>

| Feature | Description |
|:---:|:---|
| 📊 **Multi-dimensional Checks** | Completeness, uniqueness, accuracy, consistency |
| ⏰ **Timeliness Inspection** | Configure update cycles; auto-detect stale data |
| 📋 **Schema Compliance** | Detect missing comments, missing primary keys, etc. |
| 📅 **Scheduled Task Management** | Celery + Redis async queue with Cron support |
| 📄 **Report Generation** | Auto-generate PDF quality reports with AI analysis |
| 🔗 **Multi-datasource Support** | PostgreSQL, MySQL, Oracle, DM (Dameng), SQLite |

---

## 🛠 Tech Stack

<div align="center">

| Component | Version | Purpose |
|:----:|:----:|:----:|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.8+ | Backend language |
| ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) | 3.0.3 | Web framework |
| ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) | 2.0.36 | ORM |
| ![Celery](https://img.shields.io/badge/-Celery-37814A?logo=celery&logoColor=white) | 5.4.0 | Async task queue |
| ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white) | 16.x | Primary database |
| ![Redis](https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white) | 6.x | Cache & message queue |

</div>

---

## 📁 Project Structure

```
data-exploration/
│
├── 📄 app.py                      # Flask application entry point
├── 📄 init_nacos_database.py      # Database initialization script
├── 📄 requirements.txt            # Python dependencies
├── 🔧 gunicorn_control.sh         # Gunicorn start/stop script
├── 🔧 scheduler_control.sh        # Scheduler start script
├── 🔧 scheduler_quality_start.sh  # Quality scheduler start script
│
└── 📂 backend/
    ├── ⚙️  config.py               # App config (DB / Redis / Scheduler)
    ├── ⚙️  config.yaml             # Configuration file
    ├── 🛠  utils.py                # Utilities (crypto, pagination, decorators)
    ├── 📂 database/               # SQLAlchemy models
    ├── 📂 routers/                # Flask Blueprint routes
    │   ├── v1.py                  #   Rules, datasource, schedule, quality reports
    │   ├── v2.py ~ v4.py          #   Exploration APIs v2–v4
    │   ├── exploration.py         #   Core exploration APIs
    │   ├── quality_inspection.py  #   Quality inspection config
    │   ├── auth.py                #   JWT authentication
    │   └── ...
    ├── 📂 service/                # Business logic layer
    ├── 📂 celery/                 # Celery async tasks
    ├── 📂 llm/                    # LLM integration (OpenAI)
    ├── 📂 expand/                 # Data preprocessing extensions
    ├── 📂 template/               # Report templates
    ├── 📂 response/               # Unified response format
    └── 📂 sql/                    # Database init SQL files
```

---

## 🚀 Quick Start

### 📌 Prerequisites

> - **Python** 3.8+
> - **PostgreSQL** 16+
> - **Redis** 6+
> - **Oracle Instant Client** *(optional — required for Oracle datasource)*

### 📝 Configuration

Edit `backend/config.yaml`:

```yaml
# ── Database (PostgreSQL — stores platform data) ──────────────
database:
  host: 127.0.0.1
  port: 5432
  user: postgres
  password: your_password

# ── Redis ─────────────────────────────────────────────────────
redis:
  host: 127.0.0.1
  port: 6379
  password: your_redis_password   # remove if no password

# ── Scheduler ─────────────────────────────────────────────────
scheduler:
  thread_num: 20    # thread pool size
  process_num: 5    # process pool size
  max_instances: 3  # max concurrent instances per job

# ── File Storage ──────────────────────────────────────────────
report_file: /data/reports/
UPLOAD_FOLDER: /data/uploads/
```

### 🔐 Environment Variables

> ⚠️ **In production, always set secrets via environment variables — never commit them to version control!**

```bash
# JWT signing secret
export JWT_SECRET_KEY="your-strong-random-jwt-secret"

# Fernet encryption key (for password encryption/decryption)
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

### 📦 Install Dependencies

```bash
# Online install
pip install -r requirements.txt

# Offline install
tar -zxvf data-exploration.tar.gz -C venv_offline
source venv_offline/bin/activate
```

### 🗃 Initialize Database

```bash
# Run once on first deployment
python init_nacos_database.py
```

### ▶️ Start the Service

```bash
# Start web service (Gunicorn)
./gunicorn_control.sh start

# Stop web service
./gunicorn_control.sh stop

# Start task scheduler
./scheduler_control.sh start

# View logs
tail -f error.log
```

**Development mode:**

```bash
python app.py
# Listens on http://0.0.0.0:5000
```

---

## 🏭 Offline Deployment

### 🐳 Install Docker (Offline)

```bash
tar -zxvf docker-20.10.0.tgz && cp docker/* /usr/bin/
vi /usr/lib/systemd/system/docker.service
```

<details>
<summary>📋 Click to expand docker.service content</summary>

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

</details>

```bash
systemctl daemon-reload && systemctl enable docker && systemctl start docker
docker info
```

### 📦 Load Offline Images

```bash
docker load -i postgre16.tar && bash postgres_docker_run.sh
docker load -i redis-6.0.8.tar && bash redis6.0.8_run.sh
docker load -i nginx.tar   # optional
```

### ☕ Install JDK Offline

```bash
tar -zxvf jdk-8u171-linux-x64.tar.gz -C /opt/

cat >> /etc/profile << 'EOF'
export JAVA_HOME=/opt/jdk1.8.0_171
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
EOF

source /etc/profile && java -version
```

---

## ⚙️ Scheduler Modules

The platform uses two complementary scheduling mechanisms:

```
┌─────────────────────────────────────────────────────┐
│                  Scheduler Architecture             │
│                                                     │
│  HTTP Request                                       │
│       │                                             │
│       ▼                                             │
│  scheduler_redis/          backend/celery/          │
│  ┌─────────────┐  publish  ┌──────────────┐        │
│  │  Redis      │ ────────► │ Celery Worker│        │
│  │  Pub/Sub    │           │ Execute Tasks│        │
│  │  Dynamic    │           │              │        │
│  └─────────────┘           └──────────────┘        │
└─────────────────────────────────────────────────────┘
```

```bash
# Start Celery Worker
cd backend/celery && python run_worked.py

# Start Celery Beat (periodic trigger)
python run_beat.py
```

---

## 🗄 Oracle Support

```bash
export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH

# Make it permanent
echo 'export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 👨‍💻 Development Guide

### 🗺 API Route Reference

| Prefix | Module | Description |
|:-------|:-------|:------------|
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

### 💻 Local Development

```bash
# 1. Clone the repo
git clone https://github.com/teng00123/data-exploration.git
cd data-exploration

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export JWT_SECRET_KEY="dev-secret-key"
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# 4. Edit backend/config.yaml, then start
python app.py
```

### 🤝 Contributing

1. 🍴 Fork the repository
2. 🌿 Create a feature branch: `git checkout -b feature/your-feature`
3. 💾 Commit your changes: `git commit -m 'feat: add your feature'`
4. 📤 Push to the branch: `git push origin feature/your-feature`
5. 🔁 Open a Pull Request

---

<div align="center">

<br/>

*For issues or questions, please open a [GitHub Issue](https://github.com/teng00123/data-exploration/issues).*

<br/>

Made with ❤️ by the Data Exploration Team

</div>
