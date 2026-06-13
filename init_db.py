"""
数据库初始化脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DATABASE_TYPE, EXCEL_DATA_PATH, EXCEL_FOLLOW_UP_PATH, EXCEL_DAILY_TASK_PATH
from src.database.excel_db import ExcelDatabase
from src.database.mysql_db import MySQLDatabase

def init_database():
    """初始化数据库"""
    print(f"Initializing {DATABASE_TYPE} database...")
    
    if DATABASE_TYPE == 'mysql':
        db = MySQLDatabase(
            host='localhost',
            port=3306,
            user='root',
            password='password',
            database='customer_manager'
        )
    else:
        db = ExcelDatabase(
            customer_path=EXCEL_DATA_PATH,
            follow_up_path=EXCEL_FOLLOW_UP_PATH,
            daily_task_path=EXCEL_DAILY_TASK_PATH
        )
    
    if db.init_db():
        print("✓ Database initialized successfully!")
        print(f"  - Database Type: {DATABASE_TYPE}")
        if DATABASE_TYPE == 'excel':
            print(f"  - Customer Data: {EXCEL_DATA_PATH}")
            print(f"  - Follow-up Data: {EXCEL_FOLLOW_UP_PATH}")
            print(f"  - Daily Task Data: {EXCEL_DAILY_TASK_PATH}")
    else:
        print("✗ Failed to initialize database")
        sys.exit(1)

if __name__ == '__main__':
    init_database()
