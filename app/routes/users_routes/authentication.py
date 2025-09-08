from app.middleware.auth_handler import verify_token
from . import *
from app.models.user import User
from fastapi import Request

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter(redirect_slashes=False)

@router.post("/login/", include_in_schema=False)
@router.post("/login", tags=["Authentication"])
async def login_route(request: Request):
    # Accept both JSON (username/password) and form-encoded (OAuth2) payloads
    content_type = request.headers.get("content-type", "").lower()
    if content_type.startswith("application/json"):
        payload = await request.json()
        credentials = {"username": payload.get("username"), "password": payload.get("password")}
    else:
        form = await request.form()
        credentials = {"username": form.get("username"), "password": form.get("password")}

    return login(credentials)

@router.get("/validate-token/", include_in_schema=False)
@router.get("/validate-token", tags=["Authentication"])
async def validate_token(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = payload.get("sub")
    is_superuser = False
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user:
            is_superuser = bool(user.is_superuser)
    except Exception:
        # Mantém compatibilidade: ainda retorna válido se o token é válido
        pass
    return {"valid": True, "user": user_id, "is_superuser": is_superuser}
