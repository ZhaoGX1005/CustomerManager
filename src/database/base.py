"""
数据库基类 - 抽象接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

class DatabaseBase(ABC):
    """
    数据库基类，定义通用接口
    所有具体数据库实现（Excel、MySQL）都继承此类
    """
    
    @abstractmethod
    def init_db(self) -> bool:
        """初始化数据库"""
        pass
    
    # ==================== 客户管理 ====================
    @abstractmethod
    def add_customer(self, name: str, phone: str = '', email: str = '', 
                     company: str = '', position: str = '', address: str = '', 
                     remark: str = '') -> bool:
        """添加客户"""
        pass
    
    @abstractmethod
    def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """获取客户信息"""
        pass
    
    @abstractmethod
    def get_all_customers(self, page: int = 1, per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        """获取所有客户，返回 (客户列表, 总数)"""
        pass
    
    @abstractmethod
    def search_customers(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索客户"""
        pass
    
    @abstractmethod
    def update_customer(self, customer_id: int, **kwargs) -> bool:
        """更新客户信息"""
        pass
    
    @abstractmethod
    def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        pass
    
    # ==================== 跟进维护 ====================
    @abstractmethod
    def add_follow_up(self, customer_id: int, content: str, 
                      follow_up_date: datetime, 
                      next_follow_up_date: Optional[datetime] = None) -> bool:
        """添加跟进记录"""
        pass
    
    @abstractmethod
    def get_follow_up(self, follow_up_id: int) -> Optional[Dict[str, Any]]:
        """获取跟进记录"""
        pass
    
    @abstractmethod
    def get_customer_follow_ups(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户的跟进记录"""
        pass
    
    @abstractmethod
    def get_pending_reminders(self) -> List[Dict[str, Any]]:
        """获取待提醒的跟进记录"""
        pass
    
    @abstractmethod
    def update_follow_up(self, follow_up_id: int, **kwargs) -> bool:
        """更新跟进记录"""
        pass
    
    @abstractmethod
    def delete_follow_up(self, follow_up_id: int) -> bool:
        """删除跟进记录"""
        pass
    
    # ==================== 每日工作 ====================
    @abstractmethod
    def add_daily_task(self, task_name: str, task_date: datetime, 
                       priority: str = 'medium', 
                       description: str = '') -> bool:
        """添加日常任务"""
        pass
    
    @abstractmethod
    def get_daily_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取任务"""
        pass
    
    @abstractmethod
    def get_daily_tasks(self, task_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """获取指定日期的任务，不指定则获取今天的"""
        pass
    
    @abstractmethod
    def get_tasks_by_status(self, status: str, task_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """按状态获取任务"""
        pass
    
    @abstractmethod
    def update_daily_task(self, task_id: int, **kwargs) -> bool:
        """更新任务"""
        pass
    
    @abstractmethod
    def complete_daily_task(self, task_id: int) -> bool:
        """完成任务"""
        pass
    
    @abstractmethod
    def delete_daily_task(self, task_id: int) -> bool:
        """删除任务"""
        pass
    
    @abstractmethod
    def get_task_stats(self, task_date: Optional[datetime] = None) -> Dict[str, Any]:
        """获取任务统计信息"""
        pass
