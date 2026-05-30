import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..config import settings
from ..exceptions.app_exception import AppException


RESEND_SEND_EMAIL_URL = "https://api.resend.com/emails"

resend_api_key_not_configured_exception = AppException(
    status_code=500,
    error_code="RESEND_API_KEY_NOT_CONFIGURED",
    error_message="RESEND_API_KEY is not configured",
)

resend_email_send_failed_exception = AppException(
    status_code=502,
    error_code="RESEND_EMAIL_SEND_FAILED",
    error_message="Failed to send email with Resend",
)

resend_api_unreachable_exception = AppException(
    status_code=503,
    error_code="RESEND_API_UNREACHABLE",
    error_message="Failed to reach Resend API",
)


def send_email(from_email: str, to_email: str, message: str, subject: str) -> None:
    try:
        api_key = settings.RESEND_API_KEY
    except AttributeError:
        raise resend_api_key_not_configured_exception

    if not api_key:
        raise resend_api_key_not_configured_exception

    payload = json.dumps(
        {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "text": message,
        }
    ).encode("utf-8")
    request = Request(
        RESEND_SEND_EMAIL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request) as response:
            response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AppException(
            status_code=resend_email_send_failed_exception.status_code,
            error_code=resend_email_send_failed_exception.error_code,
            error_message=resend_email_send_failed_exception.error_message,
            error=detail,
        ) from exc
    except URLError:
        raise resend_api_unreachable_exception
