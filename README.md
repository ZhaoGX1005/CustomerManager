# 客户管理系统 (CustomerManager)

一个轻量级、可扩展的客户管理系统，支持本地运行和 Docker 容器部署。

## 📋 功能模块

1. **客户信息管理** - 录入、编辑、查询、删除客户信息
2. **客户跟进维护** - 设置跟进提醒、查看跟进历史、自动提醒通知
3. **每日工作必做** - 日常工作任务清单、任务状态跟踪、每日统计

## 🛠️ 技术栈

- **语言**: Python 3.9+
- **Web 框架**: Flask
- **数据库**: 
  - 初期: Excel (openpyxl)
  - 升级: MySQL (SQLAlchemy + PyMySQL)
- **部署**: Docker & Docker Compose

## 📦 安装与运行

### 方式一: 本地运行

#### 前置条件
- Python 3.9 或更高版本
- pip

#### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/ZhaoGX1005/CustomerManager.git
cd CustomerManager

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 初始化数据库（首次运行）
python init_db.py

# 6. 运行应用
python main.py
```

#### 本地访问
- Web 界面: http://localhost:5000
- API 文档: http://localhost:5000/api/docs

### 方式二: Docker 运行（Excel 数据库）

```bash
# 构建镜像
docker build -t customer-manager:latest .

# 运行容器
docker run -p 5000:5000 -v $(pwd)/data:/app/data customer-manager:latest
```

### 方式三: Docker Compose 运行（完整栈 - Excel）

```bash
docker compose -f docker-compose.yml up -d
```

访问: http://localhost:5000

### 方式四: Docker Compose 运行（MySQL 数据库）

```bash
# 使用 MySQL 配置
docker compose -f docker-compose.mysql.yml up -d
```

这将启动：
- Flask 应用 (http://localhost:5000)
- MySQL 数据库 (localhost:3306)
- phpMyAdmin 管理界面 (http://localhost:8080)

## 🔄 数据库切换指南

### 从 Excel 切换到 MySQL

#### 步骤 1: 修改配置文件

编辑 `config.py`：

```python
# 改为
DATABASE_TYPE = 'mysql'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'customer_manager'
```

#### 步骤 2: 创建 MySQL 数据库

```bash
python migrate_to_mysql.py
```

这个脚本会：
- 创建 MySQL 数据库和表
- 自动迁移 Excel 中的数据到 MySQL

#### 步骤 3: 重启应用

```bash
# 本地
python main.py

# Docker
docker-compose -f docker-compose.mysql.yml restart
```

## 📂 项目结构

```
CustomerManager/
├── README.md                          # 项目说明
├── requirements.txt                   # Python 依赖
├── config.py                          # 配置文件
├── main.py                            # 主入口
├── init_db.py                         # ��据库初始化
├── migrate_to_mysql.py                # Excel 到 MySQL 迁移脚本
│
├── Dockerfile                         # Docker 镜像配置
├── docker-compose.yml                 # Docker Compose 配置 (Excel)
├── docker-compose.mysql.yml           # Docker Compose 配置 (MySQL)
│
├── src/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py                    # 数据库基类
│   │   ├── excel_db.py                # Excel 实现
│   │   └── mysql_db.py                # MySQL 实现
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py                # 客户信息模型
│   │   ├── follow_up.py               # 跟进维护模型
│   │   └── daily_task.py              # 每日工作模型
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── customer_service.py        # 客户信息服务
│   │   ├── follow_up_service.py       # 跟进维护服务
│   │   ├── daily_task_service.py      # 每日工作服务
│   │   └── notification_service.py    # 提醒通知服务
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py                  # API 路由
│   │   └── utils.py                   # API 工具函数
│   │
│   └── ui/
│       ├── __init__.py
│       └── templates/                 # HTML 模板
│           ├── base.html
│           ├── customer_list.html
│           ├── follow_up_list.html
│           └── daily_tasks.html
│
├── data/
│   ├── customers.xlsx                 # Excel 数据文件
│   └── .gitkeep
│
└── tests/
    ├── __init__.py
    └── test_services.py
```

## 🚀 快速开始

### 1. 首次运行 - 本地 Excel

```bash
# 创建虚拟环境并安装依赖
python -m venv venv
source venv/bin/activate  # 或 venv\Scripts\activate (Windows)
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 运行应用
python main.py
```

### 2. 添加客户信息

访问 http://localhost:5000，在"客户管理"页面添加新客户

### 3. 设置跟进提醒

在"客户跟进"页面为客户设置提醒，系统会自动提醒

### 4. 管理每日工作

在"每日工作"页面管理日常任务，查看完成情况

### 5. 升级到 MySQL

```bash
python migrate_to_mysql.py
# 修改 config.py 中的 DATABASE_TYPE
python main.py
```

## 📝 API 接口

### 客户管理

```
GET    /api/customers              - 获取所有客户
POST   /api/customers              - 创建新客户
GET    /api/customers/<id>         - 获取客户详情
PUT    /api/customers/<id>         - 更新客户信息
DELETE /api/customers/<id>         - 删除客户
```

### 客户跟进

```
GET    /api/follow-ups             - 获取跟进列表
POST   /api/follow-ups             - 创建跟进记录
GET    /api/follow-ups/<id>        - 获取跟进详情
PUT    /api/follow-ups/<id>        - 更新跟进记录
DELETE /api/follow-ups/<id>        - 删除跟进记录
GET    /api/follow-ups/reminders   - 获取提醒列表
```

### 每日工作

```
GET    /api/daily-tasks            - 获取今日任务
POST   /api/daily-tasks            - 创建任务
PUT    /api/daily-tasks/<id>       - 更新任务状态
GET    /api/daily-tasks/stats      - 获取统计信息
```

## 🔧 配置说明

编辑 `config.py` 自定义以下内容：

```python
# 数据库类型: 'excel' 或 'mysql'
DATABASE_TYPE = 'excel'

# Flask 应用配置
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Excel 配置
EXCEL_DATA_PATH = './data/customers.xlsx'

# MySQL 配置
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'customer_manager'
```

## 🐳 Docker 部署说明

### Excel 模式

```bash
docker-compose up -d
```

### MySQL 模式

```bash
docker-compose -f docker-compose.mysql.yml up -d
```

### 查看日志

```bash
docker-compose logs -f app
```

### 停止容器

```bash
docker-compose down
```

## 📊 数据库架构

### 客户信息表 (customers)
- 客户ID、名称、电话、邮箱、公司、职位、备注

### 跟进维护表 (follow_ups)
- 跟进ID、客户ID、跟进内容、跟进时间、下次跟进时间、提醒状态

### 每日工作表 (daily_tasks)
- 任务ID、任务名称、日期、优先级、状态、完成时间

## 🔒 功能扩展

系统设计易于扩展，添加新功能步骤：

1. 在 `src/models/` 创建新模型
2. 在 `src/services/` 创建业务逻辑
3. 在 `src/database/` 添加数据库操作
4. 在 `src/api/` 添加 API 路由
5. 在 `src/ui/templates/` 添加前端模板

## 📄 许可证

MIT License

## 👤 作者

ZhaoGX1005

## 🤝 支持

如有问题或建议，请提交 Issue 或 PR。
