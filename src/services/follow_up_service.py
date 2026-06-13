"""
客户跟进维护服务
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.database.base import DatabaseBase

class FollowUpService:
    """跟进维护服务"""
    
    def __init__(self, db: DatabaseBase):
        self.db = db
    
    def create(self, customer_id: int, content: str, 
               follow_up_date: str, next_follow_up_date: Optional[str] = None) -> bool:
        """创建跟进记录"""
        try:
            fup_date = datetime.fromisoformat(follow_up_date) if isinstance(follow_up_date, str) else follow_up_date
            nfup_date = datetime.fromisoformat(next_follow_up_date) if next_follow_up_date and isinstance(next_follow_up_date, str) else next_follow_up_date
            return self.db.add_follow_up(customer_id, content, fup_date, nfup_date)
        except Exception as e:
            print(f"Error creating follow-up: {e}")
            return False
    
    def get_by_id(self, follow_up_id: int) -> Optional[Dict[str, Any]]:
        """根据 ID 获取跟进记录"""
        return self.db.get_follow_up(follow_up_id)
    
    def get_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户的所有跟进记录"""
        return self.db.get_customer_follow_ups(customer_id)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有跟进记录"""
        return self.db.get_customer_follow_ups(0)  # 获取所有
    
    def get_pending_reminders(self) -> List[Dict[str, Any]]:
        """获取待提醒的跟进记录"""
        return self.db.get_pending_reminders()
    
    def update(self, follow_up_id: int, **kwargs) -> bool:
        """更新跟进记录"""
        return self.db.update_follow_up(follow_up_id, **kwargs)
    
    def delete(self, follow_up_id: int) -> bool:
        """删除跟进记录"""
        return self.db.delete_follow_up(follow_up_id)
