from app.middleware.auth_handler import verify_token
from . import *

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login")
def login_route(data: dict):
    logging.info(data)
    return login(data)

@router.get("/validate-token")
async def validate_token(payload: dict = Depends(verify_token)):
    return {"valid": True, "user": payload.get("sub")}