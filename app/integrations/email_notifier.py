import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional


class EmailNotifier:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        use_tls: bool = True,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls


    # Create email message
    def _build_message(
        self,
        subject: str,
        sender: str,
        recipients: List[str],
        body: str,
        html: Optional[str] = None,
    ) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        # Plain text
        msg.attach(MIMEText(body, "plain"))

        # Optional HTML
        if html:
            msg.attach(MIMEText(html, "html"))

        return msg


    # Send email
    def send_email(
        self,
        subject: str,
        sender: str,
        recipients: List[str],
        body: str,
        html: Optional[str] = None,
    ) -> bool:
        message = self._build_message(subject, sender, recipients, body, html)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()

                server.login(self.username, self.password)
                server.sendmail(sender, recipients, message.as_string())

            return True
        except Exception:
            return False


# Convenience function
def send_alert_email(
    smtp_config: dict,
    recipients: List[str],
    subject: str,
    message: str,
) -> bool:
    notifier = EmailNotifier(
        smtp_server=smtp_config.get("smtp_server"),
        smtp_port=smtp_config.get("smtp_port", 587),
        username=smtp_config.get("username"),
        password=smtp_config.get("password"),
        use_tls=smtp_config.get("use_tls", True),
    )

    return notifier.send_email(
        subject=subject,
        sender=smtp_config.get("sender"),
        recipients=recipients,
        body=message,
    )
