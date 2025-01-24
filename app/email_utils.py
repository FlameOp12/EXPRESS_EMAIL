import os
import asyncio
import logging
import base64
from typing import List, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from aiosmtplib import send
from app.email_schema import EmailAttachment
from dotenv import load_dotenv


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def create_multipart_message(
    subject: str,
    body: str,
    sender: str,
    recipients: List[str],
    attachments: Optional[List[EmailAttachment]] = None,
    embedded_links: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> MIMEMultipart:
    """
    Create a multipart email message with advanced features.
    """
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ', '.join(recipients)

    # Add CC and BCC if provided
    if cc:
        message['Cc'] = ', '.join(cc)
    if bcc:
        message['Bcc'] = ', '.join(bcc)

    message['Subject'] = subject

    # Add body
    body_with_links = body
    if embedded_links:
        body_with_links += "\n\nAdditional Links:\n" + "\n".join(embedded_links)

    message.attach(MIMEText(body_with_links, 'html'))

    # Add attachments
    if attachments:
        for attachment in attachments:
            decoded_content = base64.b64decode(attachment.content)

            if attachment.mime_type.startswith('image/'):
                mime_subtype = attachment.mime_type.split('/')[1]  # Extract MIME subtype
                part = MIMEImage(decoded_content, _subtype=mime_subtype, name=attachment.filename)
            elif attachment.mime_type.startswith('application/'):
                part = MIMEApplication(decoded_content, name=attachment.filename)
            else:
                part = MIMEApplication(decoded_content, name=attachment.filename)

            part['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
            message.attach(part)

    return message

async def send_individual_email(
    recipient: str,
    message: MIMEMultipart,
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
) -> bool:
    """Send individual email with robust error handling."""
    try:
        await send(
            message,
            hostname=smtp_server,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            start_tls=True,
        )
        logger.info(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        return False

async def send_email(
    subject: str,
    body: str,
    recipients: List[str],
    attachments: Optional[List[EmailAttachment]] = None,
    embedded_links: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
):
    """
    Send emails concurrently with advanced features.
    """
    # Load SMTP credentials dynamically
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    all_recipients = recipients.copy()
    if cc:
        all_recipients.extend(cc)
    if bcc:
        all_recipients.extend(bcc)

    # Create multipart message
    message = create_multipart_message(
        subject=subject,
        body=body,
        sender=smtp_user,
        recipients=recipients,
        attachments=attachments,
        embedded_links=embedded_links,
        cc=cc,
        bcc=bcc
    )

    # Limit concurrent tasks
    semaphore = asyncio.Semaphore(10)

    async def send_with_semaphore(recipient):
        async with semaphore:
            return await send_individual_email(
                recipient, message, smtp_server, smtp_port, smtp_user, smtp_password
            )

    # Send emails concurrently
    results = await asyncio.gather(
        *[send_with_semaphore(recipient) for recipient in all_recipients],
        return_exceptions=True
    )

    # Log results
    successful = sum(1 for result in results if result is True)
    failed = len(all_recipients) - successful
    logger.info(f"Email send summary: Successful: {successful}, Failed: {failed}")
