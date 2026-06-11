"""
Configuration file for CustomerManager
支持 Excel 和 MySQL 数据库切换
"""
import os
from datetime import timedelta

# ==================== 应用配置 ====================
DEBUG = True
SECRET_KEY = 'your-secret-key-change-in-production'
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

# ==================== 数据库配置 ====================
# 数据库类型: 'excel' 或 'mysql'
DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'excel').lower()

# ==================== Excel 配置 ====================
EXCEL_DATA_PATH = os.environ.get('EXCEL_DATA_PATH', './data/customers.xlsx')
EXCEL_FOLLOW_UP_PATH = os.environ.get('EXCEL_FOLLOW_UP_PATH', './data/follow_ups.xlsx')
EXCEL_DAILY_TASK_PATH = os.environ.get('EXCEL_DAILY_TASK_PATH', './data/daily_tasks.xlsx')

# ==================== MySQL 配置 ====================
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'customer_manager')
MYSQL_CHARSET = 'utf8mb4'

# SQLAlchemy 数据库 URI
if DATABASE_TYPE == 'mysql':
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@'
        f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
        f'?charset={MYSQL_CHARSET}'
    )
else:
    SQLALCHEMY_DATABASE_URI = None

SQLALCHEMY_TRACK_MODIFICATIONS = False

# ==================== 应用功能配置 ====================
# 跟进提醒配置
REMINDER_CHECK_INTERVAL = timedelta(hours=1)  # 每小时检查一次
REMINDER_ADVANCE_DAYS = 1  # 提前1天提醒

# 分页配置
ITEMS_PER_PAGE = 20

# ==================== 文件上传配置 ====================
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

# ==================== 日志配置 ====================
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.environ.get('LOG_FILE', './logs/app.log')

# 确保日志目录存在
os.makedirs('./logs', exist_ok=True)
os.makedirs('./data', exist_ok=True)
