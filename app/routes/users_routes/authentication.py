from app.middleware.auth_handler import verify_token
from . import *
from app.models.user import User
from pydantic import BaseModel, Field, AliasChoices

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter(redirect_slashes=False)


class LoginRequest(BaseModel):
    identifier: str = Field(
        validation_alias=AliasChoices("identifier", "username", "email")
    )  # username ou email
    password: str

@router.post("/login/", include_in_schema=False)
@router.post("/login", tags=["Authentication"])
async def login_route(payload: LoginRequest):
    # Accept only JSON (username/password)
    return login({
        "identifier": payload.identifier,
        "password": payload.password,
    })

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
