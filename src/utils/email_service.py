import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from src.config import settings


class EmailService:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = settings.smtp_user
    smtp_password = settings.smtp_password

    @staticmethod
    def send_email_with_qr_code(img_file: str, to_addr: str):
        msg = MIMEMultipart()
        msg['Subject'] = 'Este es tu código QR para asistencia'
        msg['From'] = EmailService.smtp_user
        msg['To'] = to_addr
        with open(img_file, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name="qr_code.png")
        msg.attach(image)
        with smtplib.SMTP(EmailService.smtp_server, EmailService.smtp_port) as server:
            server.starttls()
            server.login(EmailService.smtp_user, EmailService.smtp_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
