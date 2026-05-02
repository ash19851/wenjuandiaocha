import json
import os
from flask import Flask, request, render_template, abort, session, redirect, url_for
from database import init_db, is_token_valid, mark_token_used, save_response, has_email_submitted
import sqlite3

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 加载问题配置
with open('questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)
    questions = questions_data['questions']

# 管理密钥
ADMIN_KEY = os.environ.get('ADMIN_KEY', 'admin123')

# 初始化数据库（确保表存在）
init_db()

# ---------- 管理员登录装饰器 ----------
def login_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ---------- 问卷页面 ----------
@app.route('/survey/<token>', methods=['GET', 'POST'])
def survey(token):
    # 获取 token 对应的邮箱
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute('SELECT email FROM tokens WHERE token = ?', (token,))
    row = c.fetchone()
    conn.close()
    if not row:
        return "无效的链接", 400
    email = row[0]

    if not is_token_valid(token) or has_email_submitted(email):
        return "该链接无效或已被使用", 400

    if request.method == 'POST':
        answers = {}
        for q in questions:
            qid = q['id']
            if q['type'] == 'rating':
                val = request.form.get(qid)
                if val:
                    answers[qid] = int(val)
                elif q.get('required', False):
                    return f"请回答问题：{q['text']}", 400
            else:
                answers[qid] = request.form.get(qid, '').strip()
        save_response(token, email, answers)
        mark_token_used(token)
        return "感谢您的参与！问卷提交成功。"

    return render_template('survey_dynamic.html', token=token, questions=questions)

# ---------- 管理员登录 ----------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        key = request.form.get('key')
        if key == ADMIN_KEY:
            session['admin_logged_in'] = True
            return redirect(url_for('report'))
        else:
            return render_template('admin_login.html', error='密钥错误')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# ---------- 报表页面 ----------
@app.route('/admin/report')
@login_required
def report():
    conn = sqlite3.connect('survey.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT email, answers, submitted_at FROM responses ORDER BY submitted_at DESC')
    rows = c.fetchall()
    conn.close()

    records = []
    for row in rows:
        answers = json.loads(row['answers'])
        records.append({
            'email': row['email'],
            'answers': answers,
            'submitted_at': row['submitted_at']
        })

    rating_questions = [q for q in questions if q['type'] == 'rating']
    text_questions = [q for q in questions if q['type'] == 'text']

    stats = {}
    for q in rating_questions:
        qid = q['id']
        scores = []
        for rec in records:
            score = rec['answers'].get(qid)
            if score is not None:
                scores.append(int(score))
        if scores:
            avg = sum(scores) / len(scores)
            distribution = {i: scores.count(i) for i in range(1, 6)}
        else:
            avg = 0
            distribution = {i: 0 for i in range(1, 6)}
        stats[qid] = {
            'text': q['text'],
            'avg': round(avg, 2),
            'distribution': distribution,
            'count': len(scores)
        }

    comments = []
    for q in text_questions:
        qid = q['id']
        for rec in records:
            comment = rec['answers'].get(qid)
            if comment and comment.strip():
                comments.append({
                    'email': rec['email'],
                    'comment': comment,
                    'submitted_at': rec['submitted_at']
                })

    return render_template('report.html',
                           stats=stats,
                           comments=comments,
                           total_count=len(records))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)