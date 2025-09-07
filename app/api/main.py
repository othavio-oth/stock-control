from app.routes.products_routes import category, chain_route, products_price_route, supplier_route, unit_measurement, unit_conversion, products
from app.routes.users_routes import seller, user, authentication, permissions, roles
from app.routes.tickets_routes import cost_center, tickets_routes
from app.routes.stock_routes import sales_route, stock_router
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from app.middleware.permission import get_current_user
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.router.redirect_slashes = False


   
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://strategy-web-inventory.vercel.app", "https://strategy-web-inventory-git-master-othaviooths-projects.vercel.app", "https://strategy-web-inventory-dqp5wdm4q-othaviooths-projects.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 
app.include_router(
    user.router,
    prefix="/users",
    dependencies=[Depends(get_current_user)],
)

# Mantém authentication sem dependência para permitir /authentication/login sem token
app.include_router(authentication.router, prefix="/authentication")

app.include_router(
    permissions.router,
    prefix="/permissions_adm",
    dependencies=[Depends(get_current_user)],
)

app.include_router(
    roles.router,
    prefix="/roles_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    chain_route.router,
    prefix="/chains_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    unit_measurement.router,
    prefix="/units_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    unit_conversion.router,
    prefix="/conversions_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    category.router,
    prefix="/categories_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    products.router,
    prefix="/products_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    supplier_route.router,
    prefix="/suppliers_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    products_price_route.router,
    prefix="/products_adm/prices",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    sales_route.router,
    prefix="/sales",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    cost_center.router,
    prefix="/cost_centers_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    tickets_routes.router,
    prefix="/tickets_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    stock_router.router,
    prefix="/stock_adm",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    seller.router,
    prefix="/sellers_adm",
    dependencies=[Depends(get_current_user)],
)

@app.get("/ping")
def ping():
    return {"msg": "pong v2"}   


class GenericalError(HTTPException):
    def __init__(self, detail="Erro interno do servidor"):
        super().__init__(status_code=500, detail=detail)

if __name__ == "__main__":
  uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True, access_log=True, timeout_keep_alive=600)
