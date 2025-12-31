"""
邮件发送模块
支持SMTP发送HTML和Markdown格式的邮件
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, Dict
import logging
import os

logger = logging.getLogger(__name__)

class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config: Dict):
        """
        初始化邮件发送器
        
        Args:
            config: 邮件配置字典，包含:
                - smtp_server: SMTP服务器地址
                - smtp_port: SMTP端口
                - use_ssl: 是否使用SSL
                - sender_email: 发件人邮箱
                - sender_password: 邮箱授权码
                - recipient_email: 收件人邮箱
        """
        self.config = config
        self.smtp_server = config.get('smtp_server', '')
        self.smtp_port = config.get('smtp_port', 465)
        self.use_ssl = config.get('use_ssl', True)
        self.sender_email = config.get('sender_email', '')
        self.sender_password = config.get('sender_password', '')
        self.recipient_email = config.get('recipient_email', '')
    
    def is_configured(self) -> bool:
        """检查邮件是否已配置"""
        return bool(
            self.smtp_server and 
            self.sender_email and 
            self.sender_password and 
            self.recipient_email
        )
    
    def send_email(self, subject: str, html_content: str, 
                   markdown_content: Optional[str] = None,
                   attachment_path: Optional[str] = None) -> bool:
        """
        发送邮件
        
        Args:
            subject: 邮件主题
            html_content: HTML格式的邮件内容
            markdown_content: Markdown格式的内容（作为纯文本备选）
            attachment_path: 附件路径（可选）
            
        Returns:
            是否发送成功
        """
        if not self.is_configured():
            logger.error("邮件配置不完整，请检查config.py中的EMAIL_CONFIG设置")
            logger.info("需要配置: smtp_server, sender_email, sender_password")
            return False
        
        try:
            # 创建邮件
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            
            # 添加纯文本版本（用于不支持HTML的邮件客户端）
            if markdown_content:
                text_part = MIMEText(markdown_content, "plain", "utf-8")
                message.attach(text_part)
            
            # 添加HTML版本
            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)
            
            # 添加附件
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    
                    filename = os.path.basename(attachment_path)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    message.attach(part)
            
            # 发送邮件
            if self.use_ssl:
                # SSL连接（端口465）
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            else:
                # TLS连接（端口587）
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            logger.info(f"邮件已成功发送到: {self.recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP认证失败，请检查邮箱地址和授权码是否正确")
            logger.info("提示: QQ/Foxmail邮箱需要使用授权码而非登录密码")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP错误: {e}")
            return False
        except Exception as e:
            logger.error(f"发送邮件时发生错误: {e}")
            return False
    
    def send_test_email(self) -> bool:
        """发送测试邮件"""
        subject = "AI Daily Digest - 测试邮件"
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #3498db;">🎉 配置成功！</h1>
            <p>恭喜！您的 AI Daily Digest 邮件发送功能已配置成功。</p>
            <p>从明天开始，您将每天收到AI领域的最新简报。</p>
            <hr>
            <p style="color: #999; font-size: 12px;">
                这是一封测试邮件，由 AI Daily Digest 系统自动发送。
            </p>
        </body>
        </html>
        """
        markdown_content = """
# 🎉 配置成功！

恭喜！您的 AI Daily Digest 邮件发送功能已配置成功。

从明天开始，您将每天收到AI领域的最新简报。

---
*这是一封测试邮件，由 AI Daily Digest 系统自动发送。*
        """
        
        return self.send_email(subject, html_content, markdown_content)


def test_email_sender():
    """测试邮件发送"""
    import sys
    sys.path.insert(0, '/home/ubuntu/ai_daily_digest')
    from config import EMAIL_CONFIG
    
    sender = EmailSender(EMAIL_CONFIG)
    
    if not sender.is_configured():
        print("邮件未配置，请先在 config.py 中填写 EMAIL_CONFIG")
        print("\n需要配置的项目:")
        print("  - sender_email: 发件人邮箱地址")
        print("  - sender_password: 邮箱授权码（非登录密码）")
        print("\n获取授权码的方法:")
        print("  QQ邮箱: 设置 -> 账户 -> POP3/SMTP服务 -> 开启并获取授权码")
        print("  163邮箱: 设置 -> POP3/SMTP/IMAP -> 开启并设置授权码")
        return
    
    print("正在发送测试邮件...")
    if sender.send_test_email():
        print("测试邮件发送成功！请检查收件箱。")
    else:
        print("测试邮件发送失败，请检查配置。")


if __name__ == "__main__":
    test_email_sender()
