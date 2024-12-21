# EXPRESS_EMAIL
# Bulk Email Sending API

This project is a FastAPI-based backend application designed for sending bulk emails with support for advanced features like attachments, CC, BCC, embedded links, and rate limiting. It includes a helper shell script for easy testing and a `.env` file for managing sensitive configurations.

---

## Features

- **Bulk Email Sending**: Send emails to multiple recipients with attachments, CC, BCC, and embedded links.
- **File Upload**: Upload and encode attachments in Base64 format.
- **Rate Limiting**: Protect the service with configurable request limits.
- **Concurrency**: Use asyncio for sending emails concurrently.
- **Environment Configuration**: Manage SMTP settings securely using a `.env` file.
- **Logging**: Comprehensive logging for debugging and email delivery tracking.

---

## Why Use This Software?

1. **Efficiency**: Send bulk emails to hundreds or thousands of recipients with minimal effort.
2. **Customizability**: Easily include attachments, embedded links, and personalize emails with CC and BCC options.
3. **Security**: Credentials are stored securely using a `.env` file, and emails are sent via a trusted SMTP server.
4. **Scalability**: Supports concurrent email sending, making it suitable for high-volume campaigns.
5. **Ease of Use**: The included script (`send_email.sh`) simplifies testing and integration.
6. **Flexibility**: Integrate seamlessly with other systems or applications via RESTful API endpoints.

---

## File Structure

### Main Components

- **`main.py`**: Contains API endpoints for sending emails and uploading attachments.
- **`email_schema.py`**: Defines data models for email requests and attachments using Pydantic.
- **`email_utils.py`**: Utility functions for constructing and sending emails.
- **`.env`**: Stores environment variables, including SMTP credentials.
- **`send_email.sh`**: A helper script to test the email-sending API.

---

## Prerequisites

1. Python 3.8+
2. [FastAPI](https://fastapi.tiangolo.com/)
3. [aiosmtplib](https://aiosmtplib.readthedocs.io/)
4. [SlowAPI](https://slowapi.readthedocs.io/)
5. [Dotenv](https://pypi.org/project/python-dotenv/)
6. Access to an SMTP server (e.g., Gmail, SendGrid)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory with the following variables:
     ```env
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     SMTP_USER=<your_email>@gmail.com
     SMTP_PASSWORD=<your_app_password>
     ```

---

## Running the Application

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be accessible at `http://127.0.0.1:8000`.

2. **Test the API**:
   - Open the Swagger UI for API documentation: `http://127.0.0.1:8000/docs`

3. **Run the helper script**:
   - Update the `send_email.sh` script with your email details (recipients, CC, BCC, attachments, subject, body).
   - Execute the script:
     ```bash
     bash send_email.sh
     ```

---

## API Endpoints

### 1. `POST /send-email/`
Send an email to multiple recipients.

**Request Body**:
```json
{
    "subject": "Your Subject",
    "body": "Your email body",
    "recipients": ["example1@example.com", "example2@example.com"],
    "cc": ["cc@example.com"],
    "bcc": ["bcc@example.com"],
    "embedded_links": ["https://example.com"],
    "attachments": [
        {
            "filename": "example.txt",
            "content": "<Base64 encoded content>",
            "mime_type": "text/plain"
        }
    ]
}
```

**Response**:
```json
{
    "message": "Email is being sent to 2 recipients",
    "recipients_count": 2
}
```

### 2. `POST /upload-attachments/`
Upload files to generate Base64-encoded attachments.

**Request**:
- Multipart/form-data with files.

**Response**:
```json
{
    "message": "Successfully uploaded 2 files",
    "attachments": [
        {"filename": "file1.png", "mime_type": "image/png"},
        {"filename": "file2.txt", "mime_type": "text/plain"}
    ]
}
```

---

## Key Dependencies

- **FastAPI**: For building APIs.
- **Pydantic**: For data validation.
- **aiosmtplib**: For sending emails asynchronously.
- **SlowAPI**: For rate limiting.
- **Python-dotenv**: For environment variable management.





---



## Contributing

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---



