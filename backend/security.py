from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
      def __init__(self, app, requests_per_minute: int = 60):
                super().__init__(app)
                self.requests_per_minute = requests_per_minute
                self.clients = {}

      async def dispatch(self, request: Request, call_next):
                client_ip = request.client.host
                current_time = time.time()
                if client_ip not in self.clients:
                              self.clients[client_ip] = []
                          self.clients[client_ip] = [t for t in self.clients[client_ip] if current_time - t < 60]
                if len(self.clients[client_ip]) >= self.requests_per_minute:
                              raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")
                          self.clients[client_ip].append(current_time)
                response = await call_next(request)
                return response

  class SecurityHeaderMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
                  response = await call_next(request)
                  response.headers["X-Frame-Options"] = "DENY"
                  response.headers["X-Content-Type-Options"] = "nosniff"
                  response.headers["X-XSS-Protection"] = "1; mode=block"
                  response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
                  response.headers["Content-Security-Policy"] = (
                      "default-src 'self'; "
                      "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://pagead2.googlesyndication.com https://adservice.google.com https://www.googletagmanager.com https://www.google-analytics.com; "
                      "connect-src 'self' https://pagead2.googlesyndication.com https://www.google-analytics.com; "
                      "frame-src 'self' https://googleads.g.doubleclick.net https://tpc.googlesyndication.com https://www.google.com; "
                      "img-src 'self' data: https://pagead2.googlesyndication.com https://www.google-analytics.com https://www.googletagmanager.com;"
                  )
                  return response

    def validate_input_sanitization(data: str) -> str:
          if not data: return ""
                import re
    clean = re.sub(r'<.*?>', '', data)
    return clean.replace("'", "''").strip()
