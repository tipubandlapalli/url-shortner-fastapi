from typing import Protocol
from pydantic import EmailStr

from email.message import EmailMessage
import smtplib

from src.config.settings import settings

class EmailService(Protocol):
    def send_password_reset_email(self, send_to: EmailStr, reset_link: str) -> None:
        ...

class ConsoleEmailService(EmailService):
    def send_password_reset_email(self, send_to: EmailStr, reset_link: str) -> None:
        print(f"Password reset link for {send_to}: {reset_link}")

class SmtpEmailService(EmailService):
    def send_password_reset_email(self, send_to: EmailStr, reset_link: str) -> None:
        if settings.SMTP_HOST is None:
            raise RuntimeError("SMTP_HOST is required when EMAIL_BACKEND=smtp")

        message = EmailMessage()
        message["Subject"] = "Reset your password"
        message["From"] = settings.EMAIL_FROM
        message["To"] = send_to
        message.set_content(
            f"Open this link to reset your password: {reset_link}\n\n" 
            "If you did not request this, you can ignore this email."
            )
        with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT)) as smtp:
            smtp.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(message)

def get_email_service() -> EmailService:
    if settings.EMAIL_BACKEND == "console":
        return ConsoleEmailService()
    else:
        return SmtpEmailService()

