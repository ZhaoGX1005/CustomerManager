"""数据模型"""
from datetime import datetime

class Customer:
    """客户模型"""
    def __init__(self, name: str, phone: str = '', email: str = '',
                 company: str = '', position: str = '', address: str = '',
                 remark: str = '', id: int = None, created_at: datetime = None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.company = company
        self.position = position
        self.address = address
        self.remark = remark
        self.created_at = created_at or datetime.now()

class FollowUp:
    """跟进记录模型"""
    def __init__(self, customer_id: int, content: str, follow_up_date: datetime,
                 next_follow_up_date: datetime = None, id: int = None,
                 reminder_status: str = 'pending', status: str = 'active'):
        self.id = id
        self.customer_id = customer_id
        self.content = content
        self.follow_up_date = follow_up_date
        self.next_follow_up_date = next_follow_up_date
        self.reminder_status = reminder_status
        self.status = status

class DailyTask:
    """每日工作任务模型"""
    def __init__(self, task_name: str, task_date: datetime,
                 priority: str = 'medium', description: str = '',
                 id: int = None, status: str = 'pending',
                 completed_at: datetime = None):
        self.id = id
        self.task_name = task_name
        self.task_date = task_date
        self.priority = priority
        self.description = description
        self.status = status
        self.completed_at = completed_at
