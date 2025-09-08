from fastapi.security import OAuth2PasswordBearer

# Single shared OAuth2 scheme for the whole app
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/login")

