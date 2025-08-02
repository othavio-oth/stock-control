import json
import os
from app.routes.products_routes import groups, unit_measurement, unit_conversion, type_registration, products, cost_taxation
from app.routes.users_routes import seller, user, authentication, permissions, roles
from app.routes.tickets_routes import cost_center, tickets_routes
from app.routes.stock_routes import stock_router
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.auth import JWTBearer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

import os
import json
from typing import List

def get_allowed_origins() -> List[str]:
    # Valor padrão garantido
    default_origins = ["http://localhost:3000"]
    
    # Tenta carregar da variável de ambiente
    env_origins = os.getenv("ALLOWED_ORIGINS")
    
    if not env_origins:
        return default_origins
    
    try:
        if env_origins.startswith("'") and env_origins.endswith("'"):
            env_origins = env_origins[1:-1]
            
        return list(set(json.loads(env_origins) + default_origins))
    except json.JSONDecodeError:
        return default_origins 
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 
app.include_router(user.router, prefix="/users",)
app.include_router(authentication.router, prefix="/authentication",)
app.include_router(permissions.router, prefix="/permissions_adm",)

app.include_router(roles.router, prefix="/roles_adm",)
app.include_router(groups.router, prefix="/groups_adm",)
app.include_router(unit_measurement.router, prefix="/units_adm",)
app.include_router(unit_conversion.router, prefix="/conversions_adm",)
app.include_router(type_registration.router, prefix="/type_registrations_adm",)
app.include_router(products.router, prefix="/products_adm",)

app.include_router(cost_taxation.router, prefix="/cost_taxations_adm",)
app.include_router(cost_center.router, prefix="/cost_centers_adm",)
app.include_router(tickets_routes.router, prefix="/tickets_adm",)
app.include_router(stock_router.router, prefix="/stock_adm",)
app.include_router(seller.router, prefix="/sellers_adm")


class GenericalError(HTTPException):
    def __init__(self, detail="Erro interno do servidor"):
        super().__init__(status_code=500, detail=detail)

if __name__ == "__main__":
  uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True, access_log=True, timeout_keep_alive=600)