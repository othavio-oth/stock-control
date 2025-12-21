from fastapi.security import HTTPBearer

# Single shared HTTP Bearer scheme for the whole app (no OAuth2 flow)
http_bearer = HTTPBearer()

