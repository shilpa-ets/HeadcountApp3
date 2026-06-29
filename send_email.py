import os
import smtplib
from pathlib import Path
from typing import Iterable, Optional, Union
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


def _normalize_recipients(value: Optional[Union[str, Iterable[str]]]):
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [item for item in value if item]


def send_jd_email(
    docx_path: str,
    recipient_email: Union[str, Iterable[str]],
    subject: str,
    body: str,
    cc: Optional[Union[str, Iterable[str]]] = None,
    bcc: Optional[Union[str, Iterable[str]]] = None,
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    html_body: Optional[str] = None,
):
    """
    Send a Job Description email using MIME with the JD .docx attached.

    Required .env values (unless passed directly):
    SMTP_SERVER=smtp.office365.com
    SMTP_PORT=587
    SMTP_USERNAME=your_email@company.com
    SMTP_PASSWORD=your_app_password_or_smtp_password
    """
    load_dotenv()

    sender_email = sender_email or os.getenv("SMTP_USERNAME")
    sender_password = sender_password or os.getenv("SMTP_PASSWORD")
    smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.office365.com")
    smtp_port = int(smtp_port or os.getenv("SMTP_PORT", 587))

    to_list = _normalize_recipients(recipient_email)
    cc_list = _normalize_recipients(cc)
    bcc_list = _normalize_recipients(bcc)
    all_recipients = to_list + cc_list + bcc_list

    if not sender_email:
        raise ValueError("SMTP sender email is missing. Set SMTP_USERNAME in .env or pass sender_email.")
    if not sender_password:
        raise ValueError("SMTP password is missing. Set SMTP_PASSWORD in .env or pass sender_password.")
    if not to_list:
        raise ValueError("At least one recipient email is required.")

    attachment_path = Path(docx_path)
    if not attachment_path.exists():
        raise FileNotFoundError(f"Attachment not found: {attachment_path}")

    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = subject

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(body, "plain", "utf-8"))
    if html_body:
        alt_part.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt_part)

    with open(attachment_path, "rb") as file_handle:
        attachment = MIMEBase(
            "application",
            "vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        attachment.set_payload(file_handle.read())

    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        f'attachment; filename="{attachment_path.name}"'
    )
    msg.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, all_recipients, msg.as_string())

    return {
        "status": "success",
        "sent_to": all_recipients,
        "attachment": str(attachment_path),
        "subject": subject,
    }
