"""Excel 数据库实现"""
import os
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from src.database.base import DatabaseBase
import logging

logger = logging.getLogger(__name__)

class ExcelDatabase(DatabaseBase):
    """使用 Excel 作为数据库的实现"""
    
    def __init__(self, customer_path: str = './data/customers.xlsx',
                 follow_up_path: str = './data/follow_ups.xlsx',
                 task_path: str = './data/daily_tasks.xlsx'):
        self.customer_path = customer_path
        self.follow_up_path = follow_up_path
        self.task_path = task_path
        self.customer_sheet = 'customers'
        self.follow_up_sheet = 'follow_ups'
        self.task_sheet = 'daily_tasks'
        
    def init_db(self) -> bool:
        """初始化 Excel 数据库文件"""
        try:
            os.makedirs(os.path.dirname(self.customer_path) or '.', exist_ok=True)
            
            # 初始化客户文件
            if not os.path.exists(self.customer_path):
                wb = Workbook()
                ws = wb.active
                ws.title = self.customer_sheet
                headers = ['ID', 'Name', 'Phone', 'Email', 'Company', 'Position', 'Address', 'Remark', 'CreatedAt', 'UpdatedAt']
                ws.append(headers)
                wb.save(self.customer_path)
                logger.info(f"Created customer file: {self.customer_path}")
            
            # 初始化跟进文件
            if not os.path.exists(self.follow_up_path):
                wb = Workbook()
                ws = wb.active
                ws.title = self.follow_up_sheet
                headers = ['ID', 'CustomerID', 'Content', 'FollowUpDate', 'NextFollowUpDate', 'ReminderStatus', 'Status', 'CreatedAt', 'UpdatedAt']
                ws.append(headers)
                wb.save(self.follow_up_path)
                logger.info(f"Created follow-up file: {self.follow_up_path}")
            
            # 初始化任务文件
            if not os.path.exists(self.task_path):
                wb = Workbook()
                ws = wb.active
                ws.title = self.task_sheet
                headers = ['ID', 'TaskName', 'TaskDate', 'Priority', 'Status', 'Description', 'CompletedAt', 'CreatedAt', 'UpdatedAt']
                ws.append(headers)
                wb.save(self.task_path)
                logger.info(f"Created task file: {self.task_path}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Excel database: {e}")
            return False
    
    # ==================== 客户管理 ====================
    def add_customer(self, name: str, phone: str = '', email: str = '',
                     company: str = '', position: str = '', address: str = '',
                     remark: str = '') -> bool:
        """添加客户"""
        try:
            wb = load_workbook(self.customer_path)
            ws = wb[self.customer_sheet]
            
            # 获取下一个ID
            max_id = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:
                    max_id = max(max_id, int(row[0]))
            
            new_id = max_id + 1
            now = datetime.now().isoformat()
            
            ws.append([new_id, name, phone, email, company, position, address, remark, now, now])
            wb.save(self.customer_path)
            logger.info(f"Added customer: {name} (ID: {new_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to add customer: {e}")
            return False
    
    def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """获取客户信息"""
        try:
            wb = load_workbook(self.customer_path)
            ws = wb[self.customer_sheet]
            headers = [cell.value for cell in ws[1]]
            
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] == customer_id:
                    return dict(zip(headers, row))
            return None
        except Exception as e:
            logger.error(f"Failed to get customer: {e}")
            return None
    
    def get_all_customers(self, page: int = 1, per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        """获取所有客户"""
        try:
            wb = load_workbook(self.customer_path)
            ws = wb[self.customer_sheet]
            headers = [cell.value for cell in ws[1]]
            
            customers = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:  # 跳过空行
                    customers.append(dict(zip(headers, row)))
            
            total = len(customers)
            start = (page - 1) * per_page
            end = start + per_page
            return customers[start:end], total
        except Exception as e:
            logger.error(f"Failed to get all customers: {e}")
            return [], 0
    
    def search_customers(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索客户"""
        try:
            wb = load_workbook(self.customer_path)
            ws = wb[self.customer_sheet]
            headers = [cell.value for cell in ws[1]]
            
            results = []
            keyword = keyword.lower()
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:  # 跳过空行
                    customer = dict(zip(headers, row))
                    # 在名称、电话、邮箱、公司中搜索
                    if (keyword in str(customer.get('Name', '')).lower() or
                        keyword in str(customer.get('Phone', '')).lower() or
                        keyword in str(customer.get('Email', '')).lower() or
                        keyword in str(customer.get('Company', '')).lower()):
                        results.append(customer)
            return results
        except Exception as e:
            logger.error(f"Failed to search customers: {e}")
            return []
    
    def update_customer(self, customer_id: int, **kwargs) -> bool:
        """更新客户信息"""
        try:
            wb = load_workbook(self.customer_path)
            ws = wb[self.customer_sheet]
            headers = [cell.value for cell in ws[1]]
            
            for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == customer_id:
                    for key, value in kwargs.items():
                        if key in headers:
                            col_idx = headers.index(key) + 1
                            ws.cell(row=idx, column=col_idx, value=value)
                    # 更新 UpdatedAt
                    updated_col = headers.index('UpdatedAt') + 1
                    ws.cell(row=idx, column=updated_col, value=datetime.now().isoformat())
                    wb.save(self.customer_path)
                    logger.info(f"Updated customer: {customer_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to update customer: {e}")
            return False
    
    def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        try:
            wb = load_workbook(self.customer_path)
            ws = wb[self.customer_sheet]
            
            for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == customer_id:
                    ws.delete_rows(idx)
                    wb.save(self.customer_path)
                    logger.info(f"Deleted customer: {customer_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete customer: {e}")
            return False
    
    # ==================== 跟进维护 ====================
    def add_follow_up(self, customer_id: int, content: str,
                      follow_up_date: datetime,
                      next_follow_up_date: Optional[datetime] = None) -> bool:
        """添加跟进记录"""
        try:
            wb = load_workbook(self.follow_up_path)
            ws = wb[self.follow_up_sheet]
            
            max_id = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:
                    max_id = max(max_id, int(row[0]))
            
            new_id = max_id + 1
            now = datetime.now().isoformat()
            next_date = next_follow_up_date.isoformat() if next_follow_up_date else ''
            
            ws.append([new_id, customer_id, content, follow_up_date.isoformat(),
                      next_date, 'pending', 'active', now, now])
            wb.save(self.follow_up_path)
            logger.info(f"Added follow-up record: {new_id} for customer {customer_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add follow-up: {e}")
            return False
    
    def get_follow_up(self, follow_up_id: int) -> Optional[Dict[str, Any]]:
        """获取跟进记录"""
        try:
            wb = load_workbook(self.follow_up_path)
            ws = wb[self.follow_up_sheet]
            headers = [cell.value for cell in ws[1]]
            
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] == follow_up_id:
                    return dict(zip(headers, row))
            return None
        except Exception as e:
            logger.error(f"Failed to get follow-up: {e}")
            return None
    
    def get_customer_follow_ups(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户的跟进记录"""
        try:
            wb = load_workbook(self.follow_up_path)
            ws = wb[self.follow_up_sheet]
            headers = [cell.value for cell in ws[1]]
            
            results = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] and row[1] == customer_id:
                    results.append(dict(zip(headers, row)))
            return results
        except Exception as e:
            logger.error(f"Failed to get customer follow-ups: {e}")
            return []
    
    def get_pending_reminders(self) -> List[Dict[str, Any]]:
        """获取待提醒的跟进记录"""
        try:
            wb = load_workbook(self.follow_up_path)
            ws = wb[self.follow_up_sheet]
            headers = [cell.value for cell in ws[1]]
            
            results = []
            now = datetime.now()
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] and row[5] == 'pending':  # ReminderStatus == 'pending'
                    follow_up = dict(zip(headers, row))
                    try:
                        next_date = datetime.fromisoformat(str(follow_up['NextFollowUpDate']))
                        if next_date <= now:
                            results.append(follow_up)
                    except:
                        pass
            return results
        except Exception as e:
            logger.error(f"Failed to get pending reminders: {e}")
            return []
    
    def update_follow_up(self, follow_up_id: int, **kwargs) -> bool:
        """更新跟进记录"""
        try:
            wb = load_workbook(self.follow_up_path)
            ws = wb[self.follow_up_sheet]
            headers = [cell.value for cell in ws[1]]
            
            for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == follow_up_id:
                    for key, value in kwargs.items():
                        if key in headers:
                            col_idx = headers.index(key) + 1
                            ws.cell(row=idx, column=col_idx, value=value)
                    updated_col = headers.index('UpdatedAt') + 1
                    ws.cell(row=idx, column=updated_col, value=datetime.now().isoformat())
                    wb.save(self.follow_up_path)
                    logger.info(f"Updated follow-up: {follow_up_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to update follow-up: {e}")
            return False
    
    def delete_follow_up(self, follow_up_id: int) -> bool:
        """删除跟进记录"""
        try:
            wb = load_workbook(self.follow_up_path)
            ws = wb[self.follow_up_sheet]
            
            for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == follow_up_id:
                    ws.delete_rows(idx)
                    wb.save(self.follow_up_path)
                    logger.info(f"Deleted follow-up: {follow_up_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete follow-up: {e}")
            return False
    
    # ==================== 每日工作 ====================
    def add_daily_task(self, task_name: str, task_date: datetime,
                       priority: str = 'medium',
                       description: str = '') -> bool:
        """添加日常任务"""
        try:
            wb = load_workbook(self.task_path)
            ws = wb[self.task_sheet]
            
            max_id = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:
                    max_id = max(max_id, int(row[0]))
            
            new_id = max_id + 1
            now = datetime.now().isoformat()
            
            ws.append([new_id, task_name, task_date.isoformat(), priority,
                      'pending', description, '', now, now])
            wb.save(self.task_path)
            logger.info(f"Added daily task: {task_name} (ID: {new_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to add daily task: {e}")
            return False
    
    def get_daily_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取任务"""
        try:
            wb = load_workbook(self.task_path)
            ws = wb[self.task_sheet]
            headers = [cell.value for cell in ws[1]]
            
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] == task_id:
                    return dict(zip(headers, row))
            return None
        except Exception as e:
            logger.error(f"Failed to get daily task: {e}")
            return None
    
    def get_daily_tasks(self, task_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """获取指定日期的任务"""
        try:
            if task_date is None:
                task_date = datetime.now()
            target_date = task_date.date().isoformat()
            
            wb = load_workbook(self.task_path)
            ws = wb[self.task_sheet]
            headers = [cell.value for cell in ws[1]]
            
            results = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:
                    task = dict(zip(headers, row))
                    try:
                        if str(task['TaskDate']).startswith(target_date):
                            results.append(task)
                    except:
                        pass
            return results
        except Exception as e:
            logger.error(f"Failed to get daily tasks: {e}")
            return []
    
    def get_tasks_by_status(self, status: str, task_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """按状态获取任务"""
        try:
            tasks = self.get_daily_tasks(task_date)
            return [t for t in tasks if t.get('Status') == status]
        except Exception as e:
            logger.error(f"Failed to get tasks by status: {e}")
            return []
    
    def update_daily_task(self, task_id: int, **kwargs) -> bool:
        """更新任务"""
        try:
            wb = load_workbook(self.task_path)
            ws = wb[self.task_sheet]
            headers = [cell.value for cell in ws[1]]
            
            for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == task_id:
                    for key, value in kwargs.items():
                        if key in headers:
                            col_idx = headers.index(key) + 1
                            ws.cell(row=idx, column=col_idx, value=value)
                    updated_col = headers.index('UpdatedAt') + 1
                    ws.cell(row=idx, column=updated_col, value=datetime.now().isoformat())
                    wb.save(self.task_path)
                    logger.info(f"Updated daily task: {task_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to update daily task: {e}")
            return False
    
    def complete_daily_task(self, task_id: int) -> bool:
        """完成任务"""
        return self.update_daily_task(task_id, Status='completed',
                                     CompletedAt=datetime.now().isoformat())
    
    def delete_daily_task(self, task_id: int) -> bool:
        """删除任务"""
        try:
            wb = load_workbook(self.task_path)
            ws = wb[self.task_sheet]
            
            for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == task_id:
                    ws.delete_rows(idx)
                    wb.save(self.task_path)
                    logger.info(f"Deleted daily task: {task_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete daily task: {e}")
            return False
    
    def get_task_stats(self, task_date: Optional[datetime] = None) -> Dict[str, Any]:
        """获取任务统计信息"""
        try:
            tasks = self.get_daily_tasks(task_date)
            total = len(tasks)
            completed = len([t for t in tasks if t.get('Status') == 'completed'])
            pending = len([t for t in tasks if t.get('Status') == 'pending'])
            in_progress = len([t for t in tasks if t.get('Status') == 'in_progress'])
            
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
