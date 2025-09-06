from app.middleware.auth_handler import verify_token
from . import *
from app.models.user import User

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter(redirect_slashes=False)

@router.post("/login" , tags=["Authentication"])
def login_route(data: dict):
    return login(data)

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
