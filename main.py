"""
客户管理系统主程序入口
"""
import logging
import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from config import *
from src.database.excel_db import ExcelDatabase
from src.database.mysql_db import MySQLDatabase
from src.services.customer_service import CustomerService
from src.services.follow_up_service import FollowUpService
from src.services.daily_task_service import DailyTaskService
from src.services.notification_service import NotificationService

# 配置日志
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object('config')

# 初始化数据库
def get_database():
    """获取数据库实例"""
    if DATABASE_TYPE == 'mysql':
        return MySQLDatabase(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
    else:
        return ExcelDatabase(
            customer_path=EXCEL_DATA_PATH,
            follow_up_path=EXCEL_FOLLOW_UP_PATH,
            daily_task_path=EXCEL_DAILY_TASK_PATH
        )

# 初始化服务
db = get_database()
db.init_db()

customer_service = CustomerService(db)
follow_up_service = FollowUpService(db)
daily_task_service = DailyTaskService(db)
notification_service = NotificationService(db)

logger.info(f"Database initialized: {DATABASE_TYPE}")
logger.info(f"Application started in {'DEBUG' if DEBUG else 'PRODUCTION'} mode")

# ==================== 健康检查 ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': DATABASE_TYPE
    }), 200

# ==================== 前端路由 ====================
@app.route('/', methods=['GET'])
def index():
    """首页"""
    return render_template('index.html')

@app.route('/customers', methods=['GET'])
def customers_page():
    """客户管理页面"""
    return render_template('customers.html')

@app.route('/follow-ups', methods=['GET'])
def follow_ups_page():
    """跟进维护页面"""
    return render_template('follow_ups.html')

@app.route('/daily-tasks', methods=['GET'])
def daily_tasks_page():
    """每日工作页面"""
    return render_template('daily_tasks.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """仪表板页面"""
    return render_template('dashboard.html')

# ==================== 客户管理 API ====================
@app.route('/api/customers', methods=['GET'])
def get_customers():
    """获取客户列表"""
    try:
        page = request.args.get('page', 1, type=int)
        customers, total = customer_service.get_all(page)
        return jsonify({
            'code': 200,
            'data': customers,
            'total': total,
            'page': page
        }), 200
    except Exception as e:
        logger.error(f"Error getting customers: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """创建客户"""
    try:
        data = request.get_json()
        success = customer_service.create(
            name=data.get('name'),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            company=data.get('company', ''),
            position=data.get('position', ''),
            address=data.get('address', ''),
            remark=data.get('remark', '')
        )
        if success:
            return jsonify({'code': 201, 'message': 'Customer created successfully'}), 201
        return jsonify({'code': 400, 'message': 'Failed to create customer'}), 400
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """获取客户详情"""
    try:
        customer = customer_service.get_by_id(customer_id)
        if customer:
            return jsonify({'code': 200, 'data': customer}), 200
        return jsonify({'code': 404, 'message': 'Customer not found'}), 404
    except Exception as e:
        logger.error(f"Error getting customer: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """更新客户信息"""
    try:
        data = request.get_json()
        success = customer_service.update(customer_id, **data)
        if success:
            return jsonify({'code': 200, 'message': 'Customer updated successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to update customer'}), 400
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """删除客户"""
    try:
        success = customer_service.delete(customer_id)
        if success:
            return jsonify({'code': 200, 'message': 'Customer deleted successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to delete customer'}), 400
    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/customers/search', methods=['GET'])
def search_customers():
    """搜索客户"""
    try:
        keyword = request.args.get('keyword', '')
        customers = customer_service.search(keyword)
        return jsonify({'code': 200, 'data': customers}), 200
    except Exception as e:
        logger.error(f"Error searching customers: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

# ==================== 跟进维护 API ====================
@app.route('/api/follow-ups', methods=['GET'])
def get_follow_ups():
    """获取跟进列表"""
    try:
        customer_id = request.args.get('customer_id', type=int)
        if customer_id:
            follow_ups = follow_up_service.get_by_customer(customer_id)
        else:
            follow_ups = follow_up_service.get_all()
        return jsonify({'code': 200, 'data': follow_ups}), 200
    except Exception as e:
        logger.error(f"Error getting follow-ups: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/follow-ups', methods=['POST'])
def create_follow_up():
    """创建跟进记录"""
    try:
        data = request.get_json()
        success = follow_up_service.create(
            customer_id=data.get('customer_id'),
            content=data.get('content'),
            follow_up_date=data.get('follow_up_date'),
            next_follow_up_date=data.get('next_follow_up_date')
        )
        if success:
            return jsonify({'code': 201, 'message': 'Follow-up created successfully'}), 201
        return jsonify({'code': 400, 'message': 'Failed to create follow-up'}), 400
    except Exception as e:
        logger.error(f"Error creating follow-up: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/follow-ups/reminders', methods=['GET'])
def get_reminders():
    """获取待提醒列表"""
    try:
        reminders = follow_up_service.get_pending_reminders()
        return jsonify({'code': 200, 'data': reminders}), 200
    except Exception as e:
        logger.error(f"Error getting reminders: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/follow-ups/<int:follow_up_id>', methods=['PUT'])
def update_follow_up(follow_up_id):
    """更新跟进记录"""
    try:
        data = request.get_json()
        success = follow_up_service.update(follow_up_id, **data)
        if success:
            return jsonify({'code': 200, 'message': 'Follow-up updated successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to update follow-up'}), 400
    except Exception as e:
        logger.error(f"Error updating follow-up: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/follow-ups/<int:follow_up_id>', methods=['DELETE'])
def delete_follow_up(follow_up_id):
    """删除跟进记录"""
    try:
        success = follow_up_service.delete(follow_up_id)
        if success:
            return jsonify({'code': 200, 'message': 'Follow-up deleted successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to delete follow-up'}), 400
    except Exception as e:
        logger.error(f"Error deleting follow-up: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

# ==================== 每日工作 API ====================
@app.route('/api/daily-tasks', methods=['GET'])
def get_daily_tasks():
    """获取今日任务"""
    try:
        tasks = daily_task_service.get_today_tasks()
        return jsonify({'code': 200, 'data': tasks}), 200
    except Exception as e:
        logger.error(f"Error getting daily tasks: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/daily-tasks', methods=['POST'])
def create_daily_task():
    """创建任务"""
    try:
        data = request.get_json()
        success = daily_task_service.create(
            task_name=data.get('task_name'),
            task_date=data.get('task_date'),
            priority=data.get('priority', 'medium'),
            description=data.get('description', '')
        )
        if success:
            return jsonify({'code': 201, 'message': 'Task created successfully'}), 201
        return jsonify({'code': 400, 'message': 'Failed to create task'}), 400
    except Exception as e:
        logger.error(f"Error creating daily task: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/daily-tasks/<int:task_id>', methods=['PUT'])
def update_daily_task(task_id):
    """更新任务"""
    try:
        data = request.get_json()
        success = daily_task_service.update(task_id, **data)
        if success:
            return jsonify({'code': 200, 'message': 'Task updated successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to update task'}), 400
    except Exception as e:
        logger.error(f"Error updating daily task: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/daily-tasks/<int:task_id>/complete', methods=['PUT'])
def complete_daily_task(task_id):
    """完成任务"""
    try:
        success = daily_task_service.complete(task_id)
        if success:
            return jsonify({'code': 200, 'message': 'Task completed successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to complete task'}), 400
    except Exception as e:
        logger.error(f"Error completing daily task: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/daily-tasks/<int:task_id>', methods=['DELETE'])
def delete_daily_task(task_id):
    """删除任务"""
    try:
        success = daily_task_service.delete(task_id)
        if success:
            return jsonify({'code': 200, 'message': 'Task deleted successfully'}), 200
        return jsonify({'code': 400, 'message': 'Failed to delete task'}), 400
    except Exception as e:
        logger.error(f"Error deleting daily task: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/daily-tasks/stats', methods=['GET'])
def get_task_stats():
    """获取任务统计"""
    try:
        stats = daily_task_service.get_stats()
        return jsonify({'code': 200, 'data': stats}), 200
    except Exception as e:
        logger.error(f"Error getting task stats: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

# ==================== 错误处理 ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'code': 404, 'message': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({'code': 500, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
