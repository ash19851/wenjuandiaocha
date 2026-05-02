import sqlite3
import json
DB_PATH = 'survey.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # tokens 表
    c.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            used BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # responses 表（新结构）
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            answers JSON,          -- 存储所有答案的JSON对象
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (token) REFERENCES tokens(token)
        )
    ''')
    conn.commit()
    conn.close()

def add_token(email, token):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO tokens (email, token) VALUES (?, ?)', (email, token))
    conn.commit()
    conn.close()

def is_token_valid(token):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT used, email FROM tokens WHERE token = ?', (token,))
    row = c.fetchone()
    conn.close()
    if row and not row[0]:
        email = row[1]
        # 检查该邮箱是否已提交过问卷
        if not has_email_submitted(email):
            return True
    return False

def has_email_submitted(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM responses WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    return row is not None

def mark_token_used(token):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE tokens SET used = 1 WHERE token = ?', (token,))
    conn.commit()
    conn.close()

def save_response(token, email, answers):
    """
    answers 是一个字典，包含各字段的值，例如：
    {
        'response_speed': 5,
        'problem_solving': 4,
        'communication': 5,
        'overall_satisfaction': 4,
        'comments': '很好'
    }
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    answers_json = json.dumps(answers, ensure_ascii=False)
    c.execute('INSERT INTO responses (token, email, answers) VALUES (?, ?, ?)',
              (token, email, answers_json))
    conn.commit()
    conn.close()