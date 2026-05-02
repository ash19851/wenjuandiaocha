import os
import uuid
import sys
from database import init_db, add_token
from send_email import send_survey_email
import openpyxl
import csv
# Excel文件路径（可根据需要修改，或通过环境变量传入）
CSV_FILE  = 'maillist.csv'

def parse_emails_from_csv(filepath):
    """
    解析 CSV 文件，提取第一列（从第二行开始）的邮箱列表。
    要求：第一列为邮箱地址，第一行为标题。
    """
    if not os.path.exists(filepath):
        print(f"错误：文件 {filepath} 不存在")
        sys.exit(1)
    
    emails = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig 可处理 BOM
        reader = csv.reader(f)
        try:
            header = next(reader)  # 跳过标题行
        except StopIteration:
            print("错误：CSV 文件为空")
            sys.exit(1)
        
        for row in reader:
            if row and row[0].strip():  # 取第一列，去除空白
                email = row[0].strip()
                if email:
                    emails.append(email)
    return emails

def main():
    # 初始化数据库（确保表存在）
    init_db()

    print(f"正在读取文件: {CSV_FILE}")
    emails = parse_emails_from_csv(CSV_FILE)
    if not emails:
        print("未找到任何邮箱地址，请检查CSV_FILE文件。")
        return

    print(f"共找到 {len(emails)} 个邮箱，开始发送...")
    success_count = 0
    fail_emails = []

    for email in emails:
        token = str(uuid.uuid4())
        try:
            # 存入数据库
            add_token(email, token)
            # 发送邮件（base_url需根据实际部署修改，例如生产环境域名）
            if send_survey_email(email, token, base_url='http://wenjuan.rinnai.com.cn:5000'):
                success_count += 1
                print(f"成功: {email}")
            else:
                fail_emails.append(email)
                print(f"失败: {email} (邮件发送失败)")
        except Exception as e:
            fail_emails.append(f"{email} (错误: {str(e)})")
            print(f"异常: {email} - {str(e)}")

    print("\n===== 发送完成 =====")
    print(f"成功: {success_count}")
    print(f"失败: {len(fail_emails)}")
    if fail_emails:
        print("失败列表:")
        for email in fail_emails:
            print(f"  - {email}")

if __name__ == '__main__':
    main()