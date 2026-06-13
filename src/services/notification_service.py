"""
提醒通知服务
"""
from src.database.base import DatabaseBase

class NotificationService:
    """提醒通知服务"""
    
    def __init__(self, db: DatabaseBase):
        self.db = db
    
    def send_reminder(self, follow_up_id: int) -> bool:
        """发送提醒（暂时为占位符）"""
        # TODO: 实现邮件或其他通知方式
        return True
    
    def check_pending_reminders(self) -> list:
        """检查待提醒的跟进"""
        return self.db.get_pending_reminders()
