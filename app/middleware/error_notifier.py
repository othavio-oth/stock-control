# import os
# import smtplib
# import ssl
# import traceback
# import logging
# from email.message import EmailMessage
# from datetime import datetime

# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import JSONResponse, Response

# logger = logging.getLogger(__name__)


# def _send_error_email(subject: str, body: str) -> None:
#     host = os.getenv("SMTP_HOST")
#     port = int(os.getenv("SMTP_PORT", "0") or 0)
#     user = os.getenv("SMTP_USER")
#     password = os.getenv("SMTP_PASSWORD")
#     email_from = os.getenv("SMTP_FROM") or user
#     email_to = os.getenv("SMTP_TO") or "otaviodelimasousa@gmail.com"

#     if not host or not port or not user or not password or not email_from:
#         logger.warning("Email not sent: SMTP not configured (set SMTP_* envs)")
#         return

#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = email_from
#     msg["To"] = email_to
#     msg.set_content(body)

#     context = ssl.create_default_context()
#     try:
#         # Prefer STARTTLS on standard ports; falls back to SSL if needed
#         with smtplib.SMTP(host, port, timeout=10) as server:
#             try:
#                 server.starttls(context=context)
#             except smtplib.SMTPException:
#                 # server may already require TLS/SSL; try SMTP_SSL path
#                 server.close()
#                 with smtplib.SMTP_SSL(host, port, context=context, timeout=10) as ssl_server:
#                     ssl_server.login(user, password)
#                     ssl_server.send_message(msg)
#                     return
#             server.login(user, password)
#             server.send_message(msg)
#     except Exception as e:
#         logger.error(f"Failed to send error email: {e}")


# class ErrorNotifierMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next) -> Response:
#         started = datetime.now().isoformat()
#         try:
#             response: Response = await call_next(request)
#             if getattr(response, "status_code", 200) >= 500:
#                 # Logar no console para facilitar debug local
#                 logger.error(
#                     "5xx response: %s %s status=%s ua=%s",
#                     request.method,
#                     request.url.path,
#                     getattr(response, "status_code", 500),
#                     request.headers.get("user-agent", ""),
#                 )
#                 # Build diagnostic email for 5xx responses
#                 subject = f"[Strategy Inventory] 5xx on {request.method} {request.url.path}"
#                 body = (
#                     f"Time: {started}Z\n"
#                     f"Method: {request.method}\n"
#                     f"Path: {request.url.path}\n"
#                     f"Query: {request.url.query}\n"
#                     f"Status: {response.status_code}\n"
#                     f"Client: {request.client.host if request.client else 'unknown'}\n"
#                     f"User-Agent: {request.headers.get('user-agent','')}\n"
#                 )
#                 _send_error_email(subject, body)
#             return response
#         except Exception:
#             tb = traceback.format_exc()
#             # Também loga o stack trace no console
#             logger.exception(
#                 "Unhandled exception on %s %s",
#                 request.method,
#                 request.url.path,
#             )
#             subject = f"[Strategy Inventory] Unhandled exception on {request.method} {request.url.path}"
#             body = (
#                 f"Time: {started}Z\n"
#                 f"Method: {request.method}\n"
#                 f"Path: {request.url.path}\n"
#                 f"Query: {request.url.query}\n"
#                 f"Client: {request.client.host if request.client else 'unknown'}\n"
#                 f"User-Agent: {request.headers.get('user-agent','')}\n\n"
#                 f"Traceback:\n{tb}"
#             )
#             _send_error_email(subject, body)
#             return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
