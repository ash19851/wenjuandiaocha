# templates.py
class EmailTemplates:
    @staticmethod
    def request_template():
        """问卷调查模板"""
        return """
     <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>上海林内IT室满意度调查</title>
    <style>
        /* 邮件兼容的样式（部分客户端可能忽略，但内联样式为主） */
        .ExternalClass, .ReadMsgBody { width: 100%; background-color: #f4f6f9; }
        body, table, td, p, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
        table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
        img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f4f6f9; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <!-- 主容器：居中且宽度受限 -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" align="center" bgcolor="#f4f6f9" style="background-color:#f4f6f9;">
        <tr>
            <td align="center" style="padding: 30px 15px;">
                <!-- 卡片内容 -->
                <table width="100%" max-width="600" cellpadding="0" cellspacing="0" border="0" align="center" style="max-width:600px; width:100%; background-color:#ffffff; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.05);">
                    <!-- 头部红色条（品牌色） -->
                    <tr>
                        <td style="background-color: #d9534f; border-radius: 16px 16px 0 0; padding: 20px 30px; text-align: center;">
                            <h1 style="margin:0; color:#ffffff; font-size: 24px; font-weight: 500; letter-spacing: 0.5px;">上海林内 IT室 满意度调查</h1>
                        </td>
                    </tr>
                    <!-- 主体内容 -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <!-- 问候语 -->
                            <p style="margin:0 0 20px; font-size: 16px; color:#2c3e50;">
                                尊敬的 <strong style="color:#d9534f;">{{target_email}}</strong>，
                            </p>
                            <p style="margin:0 0 20px; font-size: 16px; color:#34495e; line-height:1.6;">
                                感谢您使用IT服务，您的反馈对我们至关重要。请点击下方按钮填写满意度调查问卷（<span style="color:#d9534f;">链接一次性有效</span>）：
                            </p>
                            <!-- 按钮式链接 -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                                            <tr>
                                                <td align="center" bgcolor="#d9534f" style="background-color:#d9534f; border-radius: 50px;">
                                                    <a href="{{survey_link}}" target="_blank" style="display: inline-block; padding: 14px 36px; font-size: 16px; font-weight: 600; color: #ffffff; text-decoration: none; border-radius: 50px;">👉 开始填写问卷</a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            <!-- 备选链接（文本形式） -->
                            <p style="margin:20px 0 0; font-size: 14px; color:#7f8c8d; word-break:break-all;">
                                如果按钮无法点击，请复制以下链接到浏览器：<br>
                                <span style="color:#d9534f;">{{survey_link}}</span>
                            </p>
                        </td>
                    </tr>
                    <!-- 底部版权信息 -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 20px 30px; border-radius: 0 0 16px 16px; border-top: 1px solid #e9ecef; text-align: center;">
                            <p style="margin:0 0 5px; font-size: 12px; color:#95a5a6;">此为系统自动发送的邮件，请勿直接回复。</p>
                            <p style="margin:0; font-size: 12px; color:#95a5a6;">© 2026 上海林内有限公司. 版权所有.</p>
                        </td>
                    </tr>
                </table>
                <!-- 辅助说明（小字） -->
                <table width="100%" max-width="600" cellpadding="0" cellspacing="0" border="0" align="center" style="max-width:600px; width:100%; margin-top:15px;">
                    <tr>
                        <td style="padding: 10px; text-align: center; color:#b0bec5; font-size: 11px;">
                            如果您未请求此邮件，请忽略。
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """
    