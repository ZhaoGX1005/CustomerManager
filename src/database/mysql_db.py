"""
MySQL 数据库实现
"""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from src.database.base import DatabaseBase

try:
    import pymysql
    from pymysql import MySQLError
except ImportError:
    pymysql = None
    MySQLError = Exception

logger = logging.getLogger(__name__)

class MySQLDatabase(DatabaseBase):
    """
    使用 MySQL 作为数据库的实现
    """
    
    def __init__(self, host: str = 'localhost', port: int = 3306,
                 user: str = 'root', password: str = '',
                 database: str = 'customer_manager'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def _connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Connected to MySQL database")
            return True
        except MySQLError as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            return False
    
    def _get_connection(self):
        """获取连接，如果连接已断开则重新连接"""
        if self.connection is None or not self.connection.open:
            self._connect()
        return self.connection
    
    def init_db(self) -> bool:
        """初始化数据库（创建表）"""
        try:
            if not self._connect():
                return False
            
            cursor = self.connection.cursor()
            
            # 创建客户表
            create_customers_sql = """
            CREATE TABLE IF NOT EXISTS customers (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(100),
                company VARCHAR(100),
                position VARCHAR(100),
                address VARCHAR(255),
                remark TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_phone (phone),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            cursor.execute(create_customers_sql)
            
            # 创建跟进表
            create_follow_ups_sql = """
            CREATE TABLE IF NOT EXISTS follow_ups (
                id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT NOT NULL,
                content TEXT NOT NULL,
                follow_up_date DATETIME NOT NULL,
                next_follow_up_date DATETIME,
                reminder_status ENUM('pending', 'reminded', 'completed') DEFAULT 'pending',
                status ENUM('active', 'completed', 'archived') DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
                INDEX idx_customer_id (customer_id),
                INDEX idx_follow_up_date (follow_up_date),
                INDEX idx_next_follow_up_date (next_follow_up_date),
                INDEX idx_reminder_status (reminder_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            cursor.execute(create_follow_ups_sql)
            
            # 创建任务表
            create_tasks_sql = """
            CREATE TABLE IF NOT EXISTS daily_tasks (
                id INT PRIMARY KEY AUTO_INCREMENT,
                task_name VARCHAR(255) NOT NULL,
                task_date DATE NOT NULL,
                priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
                status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
                description TEXT,
                completed_at DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_task_date (task_date),
                INDEX idx_status (status),
                INDEX idx_priority (priority)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            cursor.execute(create_tasks_sql)
            
            self.connection.commit()
            logger.info("Database tables created successfully")
            return True
        except MySQLError as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    # ==================== 客户管理 ====================
    def add_customer(self, name: str, phone: str = '', email: str = '',
                     company: str = '', position: str = '', address: str = '',
                     remark: str = '') -> bool:
        """添加客户"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = """
            INSERT INTO customers (name, phone, email, company, position, address, remark)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, phone, email, company, position, address, remark))
            conn.commit()
            logger.info(f"Added customer: {name}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to add customer: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """获取客户信息"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM customers WHERE id = %s"
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchone()
            return result
        except MySQLError as e:
            logger.error(f"Failed to get customer: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def get_all_customers(self, page: int = 1, per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        """获取所有客户"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 获取总数
            cursor.execute("SELECT COUNT(*) as count FROM customers")
            result = cursor.fetchone()
            total = result['count'] if result else 0
            
            # 获取分页数据
            offset = (page - 1) * per_page
            sql = f"SELECT * FROM customers ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(sql, (per_page, offset))
            customers = cursor.fetchall()
            
            return customers or [], total
        except MySQLError as e:
            logger.error(f"Failed to get all customers: {e}")
            return [], 0
        finally:
            if cursor:
                cursor.close()
    
    def search_customers(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索客户"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            search_term = f"%{keyword}%"
            sql = """
            SELECT * FROM customers
            WHERE name LIKE %s OR phone LIKE %s OR email LIKE %s OR company LIKE %s
            ORDER BY created_at DESC
            """
            cursor.execute(sql, (search_term, search_term, search_term, search_term))
            results = cursor.fetchall()
            return results or []
        except MySQLError as e:
            logger.error(f"Failed to search customers: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def update_customer(self, customer_id: int, **kwargs) -> bool:
        """更新客户信息"""
        try:
            if not kwargs:
                return True
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 构建 UPDATE 语句
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['name', 'phone', 'email', 'company', 'position', 'address', 'remark']:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(customer_id)
            sql = f"UPDATE customers SET {', '.join(fields)} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            logger.info(f"Updated customer: {customer_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to update customer: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM customers WHERE id = %s"
            cursor.execute(sql, (customer_id,))
            conn.commit()
            logger.info(f"Deleted customer: {customer_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to delete customer: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    # ==================== 跟进维护 ====================
    def add_follow_up(self, customer_id: int, content: str,
                      follow_up_date: datetime,
                      next_follow_up_date: Optional[datetime] = None) -> bool:
        """添加跟进记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = """
            INSERT INTO follow_ups (customer_id, content, follow_up_date, next_follow_up_date)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (customer_id, content, follow_up_date, next_follow_up_date))
            conn.commit()
            logger.info(f"Added follow-up for customer: {customer_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to add follow-up: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_follow_up(self, follow_up_id: int) -> Optional[Dict[str, Any]]:
        """获取跟进记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM follow_ups WHERE id = %s"
            cursor.execute(sql, (follow_up_id,))
            result = cursor.fetchone()
            return result
        except MySQLError as e:
            logger.error(f"Failed to get follow-up: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def get_customer_follow_ups(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户的跟进记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM follow_ups WHERE customer_id = %s ORDER BY follow_up_date DESC"
            cursor.execute(sql, (customer_id,))
            results = cursor.fetchall()
            return results or []
        except MySQLError as e:
            logger.error(f"Failed to get customer follow-ups: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def get_pending_reminders(self) -> List[Dict[str, Any]]:
        """获取待提醒的跟进记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = """
            SELECT f.*, c.name as customer_name, c.phone, c.email
            FROM follow_ups f
            JOIN customers c ON f.customer_id = c.id
            WHERE f.reminder_status = 'pending'
            AND f.next_follow_up_date <= NOW()
            AND f.status = 'active'
            ORDER BY f.next_follow_up_date ASC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return results or []
        except MySQLError as e:
            logger.error(f"Failed to get pending reminders: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def update_follow_up(self, follow_up_id: int, **kwargs) -> bool:
        """更新跟进记录"""
        try:
            if not kwargs:
                return True
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['content', 'follow_up_date', 'next_follow_up_date', 'reminder_status', 'status']:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(follow_up_id)
            sql = f"UPDATE follow_ups SET {', '.join(fields)} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            logger.info(f"Updated follow-up: {follow_up_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to update follow-up: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def delete_follow_up(self, follow_up_id: int) -> bool:
        """删除跟进记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM follow_ups WHERE id = %s"
            cursor.execute(sql, (follow_up_id,))
            conn.commit()
            logger.info(f"Deleted follow-up: {follow_up_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to delete follow-up: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    # ==================== 每日工作 ====================
    def add_daily_task(self, task_name: str, task_date: datetime,
                       priority: str = 'medium',
                       description: str = '') -> bool:
        """添加日常任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = """
            INSERT INTO daily_tasks (task_name, task_date, priority, description)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (task_name, task_date, priority, description))
            conn.commit()
            logger.info(f"Added daily task: {task_name}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to add daily task: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_daily_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM daily_tasks WHERE id = %s"
            cursor.execute(sql, (task_id,))
            result = cursor.fetchone()
            return result
        except MySQLError as e:
            logger.error(f"Failed to get daily task: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def get_daily_tasks(self, task_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """获取指定日期的任务"""
        try:
            if task_date is None:
                task_date = datetime.now()
            
            target_date = task_date.date()
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM daily_tasks WHERE task_date = %s ORDER BY priority DESC, created_at ASC"
            cursor.execute(sql, (target_date,))
            results = cursor.fetchall()
            return results or []
        except MySQLError as e:
            logger.error(f"Failed to get daily tasks: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def get_tasks_by_status(self, status: str, task_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """按状态获取任务"""
        try:
            if task_date is None:
                task_date = datetime.now()
            
            target_date = task_date.date()
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM daily_tasks WHERE task_date = %s AND status = %s ORDER BY priority DESC"
            cursor.execute(sql, (target_date, status))
            results = cursor.fetchall()
            return results or []
        except MySQLError as e:
            logger.error(f"Failed to get tasks by status: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def update_daily_task(self, task_id: int, **kwargs) -> bool:
        """更新任务"""
        try:
            if not kwargs:
                return True
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['task_name', 'task_date', 'priority', 'status', 'description', 'completed_at']:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(task_id)
            sql = f"UPDATE daily_tasks SET {', '.join(fields)} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            logger.info(f"Updated daily task: {task_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to update daily task: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def complete_daily_task(self, task_id: int) -> bool:
        """完成任务"""
        return self.update_daily_task(task_id, status='completed', completed_at=datetime.now())
    
    def delete_daily_task(self, task_id: int) -> bool:
        """删除任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM daily_tasks WHERE id = %s"
            cursor.execute(sql, (task_id,))
            conn.commit()
            logger.info(f"Deleted daily task: {task_id}")
            return True
        except MySQLError as e:
            logger.error(f"Failed to delete daily task: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_task_stats(self, task_date: Optional[datetime] = None) -> Dict[str, Any]:
        """获取任务统计信息"""
        try:
            tasks = self.get_daily_tasks(task_date)
            total = len(tasks)
            completed = len([t for t in tasks if t.get('status') == 'completed'])
            pending = len([t for t in tasks if t.get('status') == 'pending'])
            in_progress = len([t for t in tasks if t.get('status') == 'in_progress'])
            
            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'in_progress': in_progress,
                'completion_rate': round(completed / total * 100, 2) if total > 0 else 0
            }
        except Exception as e:
            logger.error(f"Failed to get task stats: {e}")
            return {}
