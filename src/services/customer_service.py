"""
客户管理服务
"""
from typing import List, Dict, Any, Optional, Tuple
from src.database.base import DatabaseBase

class CustomerService:
    """客户服务"""
    
    def __init__(self, db: DatabaseBase):
        self.db = db
    
    def create(self, name: str, phone: str = '', email: str = '', 
               company: str = '', position: str = '', address: str = '', 
               remark: str = '') -> bool:
        """创建客户"""
        return self.db.add_customer(name, phone, email, company, position, address, remark)
    
    def get_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """根据 ID 获取客户"""
        return self.db.get_customer(customer_id)
    
    def get_all(self, page: int = 1, per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        """获取所有客户"""
        return self.db.get_all_customers(page, per_page)
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索客户"""
        return self.db.search_customers(keyword)
    
    def update(self, customer_id: int, **kwargs) -> bool:
        """更新客户"""
        return self.db.update_customer(customer_id, **kwargs)
    
    def delete(self, customer_id: int) -> bool:
        """删除客户"""
        return self.db.delete_customer(customer_id)
