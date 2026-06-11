-- 创建客户管理系统数据库
USE customer_manager;

-- 客户信息表
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '客户ID',
    name VARCHAR(100) NOT NULL COMMENT '客户名称',
    phone VARCHAR(20) COMMENT '电话',
    email VARCHAR(100) COMMENT '邮箱',
    company VARCHAR(100) COMMENT '公司名称',
    position VARCHAR(100) COMMENT '职位',
    address VARCHAR(255) COMMENT '地址',
    remark TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_phone (phone),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户信息表';

-- 客户跟进表
CREATE TABLE IF NOT EXISTS follow_ups (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '跟进ID',
    customer_id INT NOT NULL COMMENT '客户ID',
    content TEXT NOT NULL COMMENT '跟进内容',
    follow_up_date DATETIME NOT NULL COMMENT '跟进时间',
    next_follow_up_date DATETIME COMMENT '下次跟进时间',
    reminder_status ENUM('pending', 'reminded', 'completed') DEFAULT 'pending' COMMENT '提醒状态',
    status ENUM('active', 'completed', 'archived') DEFAULT 'active' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_follow_up_date (follow_up_date),
    INDEX idx_next_follow_up_date (next_follow_up_date),
    INDEX idx_reminder_status (reminder_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户跟进维护表';

-- 每日工作表
CREATE TABLE IF NOT EXISTS daily_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '任务ID',
    task_name VARCHAR(255) NOT NULL COMMENT '任务名称',
    task_date DATE NOT NULL COMMENT '任务日期',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium' COMMENT '优先级',
    status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '任务状态',
    description TEXT COMMENT '任务描述',
    completed_at DATETIME COMMENT '完成时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_task_date (task_date),
    INDEX idx_status (status),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='每日工作任务表';

-- 系统日志表（可选）
CREATE TABLE IF NOT EXISTS system_logs (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    log_type VARCHAR(50) NOT NULL COMMENT '日志类型',
    operation VARCHAR(100) COMMENT '操作',
    table_name VARCHAR(100) COMMENT '表名',
    record_id INT COMMENT '记录ID',
    old_value JSON COMMENT '旧值',
    new_value JSON COMMENT '新值',
    user_ip VARCHAR(50) COMMENT '用户IP',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_log_type (log_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统日志表';

-- 创建示例数据（可选）
INSERT INTO customers (name, phone, email, company, position) VALUES
('张三', '13800138000', 'zhangsan@example.com', '示例公司A', '销售主管'),
('李四', '13800138001', 'lisi@example.com', '示例公司B', '采购经理'),
('王五', '13800138002', 'wangwu@example.com', '示例公司C', '技术总监');

INSERT INTO follow_ups (customer_id, content, follow_up_date, next_follow_up_date, reminder_status) VALUES
(1, '首次沟通，了解需求', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), 'pending'),
(2, '确认合作意向', NOW(), DATE_ADD(NOW(), INTERVAL 3 DAY), 'pending'),
(3, '签署合同', NOW(), DATE_ADD(NOW(), INTERVAL 1 DAY), 'pending');

INSERT INTO daily_tasks (task_name, task_date, priority, status, description) VALUES
('完成客户跟进', CURDATE(), 'high', 'pending', '跟进本周的所有待办客户'),
('报表统计', CURDATE(), 'medium', 'pending', '统计本周销售数据'),
('会议准备', CURDATE(), 'medium', 'pending', '准备下午3点的团队会议');
