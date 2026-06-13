"""
每日工作任务服务
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.database.base import DatabaseBase

class DailyTaskService:
    """每日工作任务服务"""
    
    def __init__(self, db: DatabaseBase):
        self.db = db
    
    def create(self, task_name: str, task_date: str, 
               priority: str = 'medium', description: str = '') -> bool:
        """创建任务"""
        try:
            tdate = datetime.fromisoformat(task_date) if isinstance(task_date, str) else task_date
            return self.db.add_daily_task(task_name, tdate, priority, description)
        except Exception as e:
            print(f"Error creating daily task: {e}")
            return False
    
    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """根据 ID 获取任务"""
        return self.db.get_daily_task(task_id)
    
    def get_today_tasks(self) -> List[Dict[str, Any]]:
        """获取今天的任务"""
        return self.db.get_daily_tasks()
    
    def get_by_date(self, task_date: datetime) -> List[Dict[str, Any]]:
        """获取指定日期的任务"""
        return self.db.get_daily_tasks(task_date)
    
    def get_by_status(self, status: str) -> List[Dict[str, Any]]:
        """按状态获取任务"""
        return self.db.get_tasks_by_status(status)
    
    def update(self, task_id: int, **kwargs) -> bool:
        """更新任务"""
        return self.db.update_daily_task(task_id, **kwargs)
    
    def complete(self, task_id: int) -> bool:
        """完成任务"""
        return self.db.complete_daily_task(task_id)
    
    def delete(self, task_id: int) -> bool:
        """删除任务"""
        return self.db.delete_daily_task(task_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取任务统计"""
        return self.db.get_task_stats()
