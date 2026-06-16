import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import  settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str) -> bool:
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("Email credentials not configured. Skipping email send.")
            return False
        
        try:
            msg = MIMEMultipart()
            msg["From"] = settings.EMAIL_FROM
            msg["To"] = to_email
            msg["Subject"] = subject
            
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_order_confirmation(email: str, order_id: int, total: float):
        subject = f"Order Confirmation - #{order_id}"
        body = f"""
        Thank you for your order!
        
        Order ID: {order_id}
        Total Amount: ${total:.2f}
        
        Your order has been confirmed and will be processed shortly.
        
        Thank you for shopping with us!
        """
        return EmailService.send_email(email, subject, body)
    
    @staticmethod
    def send_shipment_notification(email: str, order_id: int, tracking_number: str):
        subject = f"Shipment Notification - Order #{order_id}"
        body = f"""
        Your order has been shipped!
        
        Order ID: {order_id}
        Tracking Number: {tracking_number}
        
        You can track your package using the tracking number above.
        
        Thank you for shopping with us!
        """
        return EmailService.send_email(email, subject, body)