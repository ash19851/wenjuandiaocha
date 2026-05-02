
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_survey_email(recipient_email, token, base_url='http://wenjuan.rinnai.com.cn:5000'):
    smtp_server = '192.168.0.83'
    smtp_port = 25
    sender_email = 'zhuming-bot@shrinnai.com'
    password = 'Rinnai@2025!'  # 邮箱授权码

    subject = 'IT满意度调查问卷'
    survey_link = f'{base_url}/survey/{token}'
    body = f"""
    您好，
    感谢您使用IT服务，请点击以下链接填写满意度调查问卷（链接一次性有效）：
    {survey_link}
    如果您无法点击，请复制地址到浏览器访问。
    谢谢！
    """
    from templates import EmailTemplates
    html_template = EmailTemplates.request_template()
    email_content = html_template.replace("{{survey_link}}", survey_link)
    email_content = email_content.replace("{{target_email}}", recipient_email)
    html_part = MIMEText(email_content, "html")
   
    
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
       # server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False















"""import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getmiallist import read_all_rows_specific_sheet
from database import init_db, add_token, is_token_valid, mark_token_used, save_response
import uuid
def send_survey_email(  base_url='http://localhost:5000'):
    # 配置邮件服务器
    SMTP_SERVER = "192.168.0.83"  # 替换为你的SMTP服务器
    SMTP_PORT = 25
    SENDER_EMAIL = "hr@shrinnai.com"  # 替换为发件人邮箱
    SENDER_PASSWORD = "Rinnai@2025!"  # 替换为应用密码或授权码
    
    # 获取发送对象清单
    target_emails  = read_all_rows_specific_sheet("maillist.xlsx")
    
    # 初始化邮件发送器
    subject = 'IT满意度调查问卷'
    campaign_name='2026 Q1~Q2 IT满意度调查问卷'
    launch_campaign(campaign_name,subject,target_emails,SENDER_EMAIL,SMTP_SERVER,SMTP_PORT,SENDER_PASSWORD,base_url)

"""






"""
def launch_campaign(campaign_name, subject, target_emails,SENDER_EMAIL,SMTP_SERVER,SMTP_PORT,SENDER_PASSWORD,base_url):
        启动邮件发送



        # 创建活动记录
        #campaign_id = self.db.create_campaign(campaign_name, subject, html_template, target_emails)
        
        print(f"开始问卷调查活动: {campaign_name}")
        print(f"目标数量: {len(target_emails)}")
        
        # 发送邮件
        success_count = 0
        for email in target_emails:
            token = str(uuid.uuid4())  # 生成唯一token
            survey_link = f'{base_url}/survey/{token}'
            
            from templates import EmailTemplates
            html_template = EmailTemplates.request_template()
            if send_phishing_email( email, subject, html_template,SENDER_EMAIL,SMTP_SERVER,SMTP_PORT,SENDER_PASSWORD,survey_link):
                add_token(email, token)
                success_count += 1
        
        print(f"活动完成: {success_count}/{len(target_emails)} 邮件发送成功")
        #return campaign_id



def send_phishing_email(target_email, subject, html_template,SENDER_EMAIL,SMTP_SERVER,SMTP_PORT,SENDER_PASSWORD,survey_link):
        发送邮件


        # 创建跟踪链接
       # tracking_link = self.create_tracking_link(target_email, campaign_id)
        
        # 替换模板中的占位符
        email_content = html_template.replace("{{survey_link}}", survey_link)
        email_content = email_content.replace("{{target_email}}", target_email)
        
        # 创建邮件
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] =SENDER_EMAIL
        message["To"] = target_email
        
        # 添加HTML版本
        html_part = MIMEText(email_content, "html")
        message.attach(html_part)
        
        try:
            # 发送邮件
            #context = ssl.create_default_context()
           # with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, target_email, message.as_string())
            
            print(f"邮件已发送至: {target_email}")
            return True
            
        except Exception as e:
            print(f"发送邮件失败 {target_email}: {str(e)}")
            return False


            """