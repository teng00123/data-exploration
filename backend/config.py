import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_sqlalchemy import SQLAlchemy
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os
import redis
import urllib.parse

# 尝试加载 .env 文件（开发环境便利，生产环境通过系统环境变量注入）
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(BASE_DIR := os.path.abspath(os.path.dirname(__file__))), '.env'))
except ImportError:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def read_config(file_path: str) -> dict:
    """读取 YAML 配置文件，敏感字段优先使用环境变量覆盖"""
    with open(file_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    # ── 数据库：环境变量优先 ──────────────────────────────────
    db_cfg = cfg.setdefault('database', {})
    db_cfg['host']     = os.environ.get('DB_HOST',     db_cfg.get('host', 'localhost'))
    db_cfg['port']     = int(os.environ.get('DB_PORT', db_cfg.get('port', 5432)))
    db_cfg['user']     = os.environ.get('DB_USER',     db_cfg.get('user', 'postgres'))
    db_cfg['password'] = os.environ.get('DB_PASSWORD', db_cfg.get('password', ''))

    # ── Redis：环境变量优先 ───────────────────────────────────
    redis_cfg = cfg.setdefault('redis', {})
    redis_cfg['host']     = os.environ.get('REDIS_HOST',     redis_cfg.get('host', '127.0.0.1'))
    redis_cfg['port']     = int(os.environ.get('REDIS_PORT', redis_cfg.get('port', 6379)))
    redis_cfg['password'] = os.environ.get('REDIS_PASSWORD', redis_cfg.get('password', ''))

    # ── 应用密钥：环境变量优先，未配置时启动失败 ──────────────
    secret_key = os.environ.get('SECRET_KEY', cfg.get('SECRET_KEY', ''))
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY is not configured. "
            "Set the SECRET_KEY environment variable or add it to .env."
        )
    cfg['SECRET_KEY'] = secret_key

    # ── OpenAI：环境变量优先 ──────────────────────────────────
    openai_cfg = cfg.setdefault('openai', {})
    openai_cfg['api_key']  = os.environ.get('OPENAI_API_KEY',  openai_cfg.get('api_key', ''))
    openai_cfg['api_base'] = os.environ.get('OPENAI_API_BASE', openai_cfg.get('api_base', 'https://api.openai.com/v1'))
    openai_cfg['model']    = os.environ.get('OPENAI_MODEL',    openai_cfg.get('model', 'gpt-3.5-turbo'))

    # ── LLM URL：环境变量优先 ─────────────────────────────────
    cfg['llm_url'] = os.environ.get('LLM_URL', cfg.get('llm_url', ''))

    # ── 文件路径：环境变量优先（修正 Windows 绝对路径问题）────
    cfg['excel_file']    = os.environ.get('EXCEL_FILE_PATH',    cfg.get('excel_file', './data_resources/'))
    cfg['ai_excel_file'] = os.environ.get('AI_EXCEL_FILE_PATH', cfg.get('ai_excel_file', './backend/template/AI_result/'))
    cfg['report_file']   = os.environ.get('REPORT_FILE_PATH',   cfg.get('report_file', './check_files/'))
    cfg['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER',      cfg.get('UPLOAD_FOLDER', './backups/'))

    return cfg


config = read_config(BASE_DIR + '/config.yaml')
db = SQLAlchemy()

scheduler = BackgroundScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(
            url=(
                f'postgresql://{config["database"]["user"]}'
                f':{urllib.parse.quote_plus(config["database"]["password"])}'
                f'@{config["database"]["host"]}:{config["database"]["port"]}/bsp-user'
            )
        )
    },
    executors={
        'default': ThreadPoolExecutor(config['scheduler']['thread_num']),
        'processpool': ProcessPoolExecutor(config['scheduler']['process_num']),
    },
    job_defaults={
        'coalesce': False,
        'misfire_grace_time': None,
        'max_instances': config['scheduler']['max_instances'],
    },
)

r = redis.Redis(
    host=config['redis']['host'],
    port=config['redis']['port'],
    db=0,
    password=config['redis']['password'] or None,
)
