from app.middleware.auth_handler import verify_token
from . import *
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter(redirect_slashes=False)

@router.post("/login/" , include_in_schema=False)
@router.post("/login" , tags=["Authentication"])
def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
    # Accept Swagger's OAuth2 password flow (form-encoded)
    credentials = {"username": form_data.username, "password": form_data.password}
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
