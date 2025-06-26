from . import *

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login")
def login_route(data: dict):
    logging.info(data)
    return login(data)