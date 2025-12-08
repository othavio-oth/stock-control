from app.routes.products_routes import category, chain_route, products_price_route, shelf_price_route, supplier_route, unit_measurement, unit_conversion, products
from app.routes.users_routes import seller, user, authentication, permissions, roles
from app.routes.tickets_routes import cost_center, tickets_routes
from app.routes.stock_routes import client_stock_route, stock_router
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.middleware.permission import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_notifier import ErrorNotifierMiddleware
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.router.redirect_slashes = False


   
app.add_middleware(ErrorNotifierMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://strategy-web-inventory.vercel.app", "https://strategy-web-inventory-git-master-othaviooths-projects.vercel.app", "https://strategy-web-inventory-git-preview-othaviooths-projects.vercel.app", "http://localhost:3000"],
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
    shelf_price_route.router,
    prefix="/products_adm/shelf-prices",
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
app.include_router(
    client_stock_route.router,
    prefix="/client_stock",
    dependencies=[Depends(get_current_user)],
)

@app.get("/ping")
def ping():
    return {"msg": "pong v2"}   


# Debug/test-only routes (enabled with ENABLE_DEBUG_ROUTES=true)
if os.getenv("ENABLE_DEBUG_ROUTES", "false").lower() == "true":
    @app.get("/_debug/error")
    def debug_error():
        raise RuntimeError("Forced error for testing ErrorNotifierMiddleware")

    @app.get("/_debug/500")
    def debug_500():
        return Response(content="Forced 500", status_code=500)


class GenericalError(HTTPException):
    def __init__(self, detail="Erro interno do servidor"):
        super().__init__(status_code=500, detail=detail)


# \-\-\-\- Padronização de erros (payload unificado) \-\-\-\-
def _build_error_payload(
    *,
    request: Request,
    status_code: int,
    message: str,
    code: str,
    details: dict | list | None = None,
):
    req_id = request.headers.get("x-request-id")
    return {
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "status_code": status_code,
        },
        "meta": {
            "path": str(request.url.path),
            "method": request.method,
            "request_id": req_id,
        },
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    payload = _build_error_payload(
        request=request,
        status_code=422,
        message="Erro de validação do payload",
        code="validation_error",
        details=exc.errors(),
    )
    return JSONResponse(status_code=422, content=payload)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Se detail já vier como dict com 'code' e 'message', preserva
    if isinstance(exc.detail, dict):
        code = exc.detail.get("code") or (
            "not_found" if exc.status_code == 404 else
            "unauthorized" if exc.status_code == 401 else
            "forbidden" if exc.status_code == 403 else
            "bad_request" if exc.status_code == 400 else
            "http_error"
        )
        message = exc.detail.get("message") or exc.detail.get("detail") or str(exc.detail)
        details = exc.detail.get("details")
    else:
        # detail é string
        message = str(exc.detail) if exc.detail else (
            "Recurso não encontrado" if exc.status_code == 404 else
            "Requisição inválida"
        )
        code = (
            "not_found" if exc.status_code == 404 else
            "bad_request" if exc.status_code == 400 else
            "http_error"
        )
        details = None

    payload = _build_error_payload(
        request=request,
        status_code=exc.status_code,
        message=message,
        code=code,
        details=details,
    )
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Evita vazar mensagens internas; log detalhado vai pelo ErrorNotifierMiddleware
    payload = _build_error_payload(
        request=request,
        status_code=500,
        message="Erro interno do servidor",
        code="internal_error",
        details=None,
    )
    return JSONResponse(status_code=500, content=payload)

if __name__ == "__main__":
  uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True, access_log=True, timeout_keep_alive=600)
