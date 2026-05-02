# IT 满意度调查系统

基于 Flask 的 IT 服务满意度调查问卷系统，支持批量邮件发送、一次性链接填写、管理员报表查看。

## 功能

- **问卷调查**：支持评分题（1-5 分）和文本意见题，每个链接一次性有效，防止重复提交
- **批量邮件发送**：读取 CSV 邮件列表，为每个收件人生成唯一的问卷链接并自动发送
- **管理后台**：管理员登录后查看答题统计（平均分、分数分布柱状图）和用户评论
- **邮件模板**：品牌化 HTML 邮件模板，含红色品牌色和响应式设计

## 项目结构

```
.
├── app.py              # Flask 主应用（路由、问卷提交、管理后台）
├── database.py         # SQLite 数据库操作（token、答卷管理）
├── send_email.py       # SMTP 邮件发送
├── send_batch.py       # 批量发送入口（从 CSV 读取收件人）
├── templates.py        # HTML 邮件模板
├── questions.json      # 问卷题目配置
├── maillist.csv        # 收件人邮箱列表
└── templates/
    ├── survey_dynamic.html  # 调查问卷填写页面
    ├── report.html          # 管理报表页面
    └── admin_login.html     # 管理员登录页面
```

## 快速开始

### 环境要求

- Python 3.8+
- Flask

### 安装依赖

```bash
pip install flask openpyxl
```

### 配置

修改 `send_email.py` 中的 SMTP 配置：

```python
smtp_server = '192.168.0.83'   # SMTP 服务器
smtp_port = 25                  # SMTP 端口
sender_email = 'your-email@example.com'
password = 'your-password'
```

通过环境变量覆盖默认配置：

- `SECRET_KEY`：Flask session 密钥（默认 `dev-secret-key-change-in-production`）
- `ADMIN_KEY`：管理员登录密钥（默认 `admin123`）

### 题库配置

编辑 `questions.json` 自定义题目，支持两种题型：

- `rating`：1-5 评分题（可设 `required: true`）
- `text`：文本意见题

### 运行

```bash
# 1. 准备收件人列表（maillist.csv，第一列邮箱）
# 2. 批量发送问卷邮件
python send_batch.py

# 3. 启动 Web 服务
python app.py
```

### 访问地址

- 问卷页面：`http://localhost:5000/survey/<token>`（邮件中的链接）
- 管理登录：`http://localhost:5000/admin/login`
- 管理报表：`http://localhost:5000/admin/report`

## 技术栈

- **后端**：Flask（Python）
- **数据库**：SQLite
- **前端**：Bootstrap 5 + Chart.js
- **邮件**：SMTP（smtplib）
