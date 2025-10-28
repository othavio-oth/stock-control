from datetime import datetime
from typing import Any, Optional, Literal, List

from fastapi import Query
from fastapi.responses import HTMLResponse
from app.controller.stock_controller.stock_movement_controller import  (
    get_all_movements,
    get_current_stock,
    reset_inventory_stock_controller,
    register_stock_loss_controller,
    register_client_sale_controller,
    get_product_entries_controller,
    delete_stock_entry_controller,
    update_stock_entry_controller,
    add_stock_bulk_controller,
    get_client_sales_history_controller,
    get_client_loss_history_controller,
    get_client_sales_and_loss_history_controller,
    get_daily_sales_and_loss_grouped_by_cost_center_controller,
    get_sales_quantity_controller,
    update_client_sale_for_day_controller,
)
from app.models.stockMovement import StockMovement
from app.schemas.stock_schemas.stock_movement_schema import (
    ClientStockResponse,
    InventoryResponse,
    StockMovementLost,
    StockMovementRead,
    SupplierPurchaseDTO,
    TotalProductStockResponse,
    RegisterClientSalesDTO,
)
from app.schemas.stock_schemas.stock_movement_schema import StockEntryRead, ClientSalesHistoryRead, ClientLossHistoryRead, ClientSalesLossHistoryRead, DailyCostCenterSalesLossGroupRead
from app.schemas.stock_schemas.stock_movement_schema import SalesQuantityResponse
from app.schemas.stock_schemas.stock_movement_schema import ClientSalesUpdateDTO, ClientSalesUpdateResult
from app.schemas.stock_schemas.stock_movement_schema import SupplierPurchaseUpdateDTO, StockEntryReadWithCost, SupplierPurchaseBulkDTO
from app.service.stock_service.stock_movement_service import StockMovementService
from . import *
router = APIRouter(redirect_slashes=False)




@router.get("/stock-movements/", include_in_schema=False)
@router.get("/stock-movements", response_model=List[StockMovementRead], tags=["Stock Movements"])
def get_stock_movements(
    db: Session = Depends(get_db),
    movement_type: Optional[Literal[
        "supplier_purchase", "to_client", "client_sale", "client_loss", "supplier_loss"
    ]] = Query(None, description="Filtrar por tipo de movimento"),
    product_id: Optional[int] = Query(None, description="Filtrar por ID do produto"),
):
    return get_all_movements(db, movement_type=movement_type, product_id=product_id)


@router.get("/stock-movements/product/{product_id}/entries/", include_in_schema=False)
@router.get(
    "/stock-movements/product/{product_id}/entries",
    response_model=List[StockEntryRead],
    tags=["Stock Movements"],
    summary="Entradas (fornecedor) por produto",
)
def get_product_entries(
    product_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_product_entries_controller(db, product_id, page, page_size)



@router.get("/stock-movements/current-stock/", include_in_schema=False)
@router.get("/stock-movements/current-stock", response_model=List[InventoryResponse], tags=["Stock Movements"])
def get_total_in_system(db: Session = Depends(get_db)):
    return get_current_stock(db)


@router.post("/stock-movements/reset-inventory/", include_in_schema=False)
@router.post("/stock-movements/reset-inventory", tags=["Stock Movements"])
def reset_inventory_stock(db: Session = Depends(get_db)):
    reset_count = reset_inventory_stock_controller(db)
    return {"reset_count": reset_count}



@router.post("/add-stock/", include_in_schema=False)
@router.post("/add-stock", response_model=StockMovementRead, status_code=status.HTTP_201_CREATED, tags=["Stock Movements"])
def add_stock( dto:SupplierPurchaseDTO, db: Session = Depends(get_db),):
    return StockMovementService.add_stock_with_cost_average(db, dto)

@router.post("/add-stock/bulk/", include_in_schema=False)
@router.post(
    "/add-stock/bulk",
    response_model=List[StockEntryReadWithCost],
    status_code=status.HTTP_201_CREATED,
    tags=["Stock Movements"],
)
def add_stock_bulk(dto: SupplierPurchaseBulkDTO, db: Session = Depends(get_db)):
    return add_stock_bulk_controller(db, dto)

@router.get(
    "/client-stock/",
    include_in_schema=False,
)

# @router.get("/stock-movements/monthly-sales-losses", 
#            response_model=List[Dict[str, Any]], 
#            tags=["Stock Movements"])
# def get_monthly_stats(
#     db: Session = Depends(get_db),
#     year: int = None
# ):
#     """
#     Endpoint para estatísticas mensais de vendas e perdas
#     """
#     return get_monthly_sales_losses_stats_controller(db, year)
    

# @router.get("/stock-movements/{product_id}", response_model=TotalProductStockResponse, tags=["Stock Movements"])
# def get_stock_products(product_id: int,db: Session = Depends(get_db), ):
#     return get_total_in_system_by_product(db, product_id)


# @router.get("/stock-movements/cost-center/{cost_center_id}/period", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
# def get_total_sold_by_cost_center_in_period(
#     cost_center_id: int,
#     start_date: datetime,
#     end_date: datetime,
#     db: Session = Depends(get_db),
# ):
#     return get_total_sold_by_cost_center_in_period_grouped_by_product(
#         db, cost_center_id, start_date, end_date
#     )
    
# @router.get("/stock-movements/cost-center/{cost_center_id}", response_model=List[TotalProductStockResponse], tags=["Stock Movements"])
# def get_cost_center_stock(
#     cost_center_id: int,
#     db: Session = Depends(get_db),
# ):
#     return get_cost_center_stock_controller(cost_center_id, db)


@router.post("/stock-movements/losses/", include_in_schema=False)
@router.post("/stock-movements/losses",response_model=StockMovementRead,status_code=status.HTTP_201_CREATED, tags=["Stock Movements"])
def create_loss_record(
    loss_data: StockMovementLost,
    db: Session = Depends(get_db)):
    try:
        return register_stock_loss_controller(db, loss_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))

@router.post("/stock-movements/sales/", include_in_schema=False)
@router.post("/stock-movements/sales",response_model=StockMovementRead,status_code=status.HTTP_201_CREATED, tags=["Stock Movements"])
def create_sale_record(
    sale_data: RegisterClientSalesDTO,
    db: Session = Depends(get_db)):
    try:
        return register_client_sale_controller(db, sale_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))


@router.delete("/stock-movements/entries/{movement_id}/", include_in_schema=False)
@router.delete(
    "/stock-movements/entries/{movement_id}",
    response_model=StockEntryRead,
    tags=["Stock Movements"],
    summary="Exclui uma entrada de estoque (compra do fornecedor)",
)
def delete_stock_entry(movement_id: int, db: Session = Depends(get_db)):
    """Exclui a última entrada SUPPLIER_PURCHASE de um produto, revertendo estoque e custo atual.
    Regras:
    - Só permite exclusão se a entrada for a mais recente para o produto.
    - Bloqueia se o estoque atual do inventário for insuficiente para reverter a entrada.
    """
    return delete_stock_entry_controller(db, movement_id)

@router.patch("/stock-movements/entries/{movement_id}/", include_in_schema=False)
@router.patch(
    "/stock-movements/entries/{movement_id}",
    response_model=StockEntryReadWithCost,
    tags=["Stock Movements"],
    summary="Edita a última entrada de estoque (compra do fornecedor) e retorna o custo médio recalculado",
)
def update_stock_entry(movement_id: int, body: SupplierPurchaseUpdateDTO, db: Session = Depends(get_db)):
    """Edita a última entrada SUPPLIER_PURCHASE de um produto, ajustando estoque pelo delta
    e recalculando o custo médio vigente. Retorna a entrada atualizada e o custo médio atual.
    """
    try:
        return update_stock_entry_controller(db, movement_id, body)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/client-sales-history/", include_in_schema=False)
@router.get(
    "/client-sales-history",
    response_model=List[ClientSalesHistoryRead],
    tags=["Client Stock"],
    summary="Histórico diário de vendas do cliente",
)
def get_client_sales_history(
    cost_center_id: int = Query(..., description="ID do cost center"),
    product_id: Optional[int] = Query(None, description="ID do produto"),
    start_date: Optional[datetime] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    sd = start_date.date() if start_date else None
    ed = end_date.date() if end_date else None
    return get_client_sales_history_controller(db, cost_center_id, product_id, sd, ed)


@router.get("/client-loss-history/", include_in_schema=False)
@router.get(
    "/client-loss-history",
    response_model=List[ClientLossHistoryRead],
    tags=["Client Stock"],
    summary="Histórico diário de perdas do cliente",
)
def get_client_loss_history(
    cost_center_id: int = Query(..., description="ID do cost center"),
    product_id: Optional[int] = Query(None, description="ID do produto"),
    start_date: Optional[datetime] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    sd = start_date.date() if start_date else None
    ed = end_date.date() if end_date else None
    return get_client_loss_history_controller(db, cost_center_id, product_id, sd, ed)


@router.get("/client-sales-loss-history/", include_in_schema=False)
@router.get(
    "/client-sales-loss-history",
    response_model=List[ClientSalesLossHistoryRead],
    tags=["Client Stock"],
    summary="Histórico diário combinado de vendas e perdas do cliente",
)
def get_client_sales_and_loss_history(
    cost_center_id: int = Query(..., description="ID do cost center"),
    product_id: Optional[int] = Query(None, description="ID do produto"),
    start_date: Optional[datetime] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    sd = start_date.date() if start_date else None
    ed = end_date.date() if end_date else None
    return get_client_sales_and_loss_history_controller(db, cost_center_id, product_id, sd, ed)


@router.get("/client-sales-loss-history/by-day/", include_in_schema=False)
@router.get(
    "/client-sales-loss-history/by-day",
    response_model=List[DailyCostCenterSalesLossGroupRead],
    tags=["Client Stock"],
    summary="Vendas e perdas por dia agrupadas por cost center",
)
def get_daily_sales_and_loss_grouped_by_cost_center(
    start_date: datetime = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="Data final (YYYY-MM-DD)"),
    product_id: Optional[int] = Query(None, description="ID do produto (opcional)"),
    cost_center_ids: Optional[List[int]] = Query(None, description="IDs de cost centers (opcional, multiplos valores)"),
    db: Session = Depends(get_db),
):
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="end_date deve ser >= start_date")
    sd = start_date.date()
    ed = end_date.date()
    ids = list(cost_center_ids) if cost_center_ids else None
    return get_daily_sales_and_loss_grouped_by_cost_center_controller(
        db,
        start_date=sd,
        end_date=ed,
        cost_center_ids=ids,
        product_id=product_id,
    )


@router.get(
    "/client-sales-loss-history/by-day/page",
    response_class=HTMLResponse,
    include_in_schema=False,
    tags=["Client Stock"],
    summary="Página HTML para visualizar vendas e perdas diárias",
)
def client_sales_loss_history_page():
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório diário de vendas e perdas</title>
    <style>
        :root { color-scheme: light dark; }
        body { font-family: Arial, sans-serif; margin: 2rem auto; max-width: 960px; padding: 0 1.5rem; }
        h1 { margin-bottom: 1rem; }
        form { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); align-items: end; margin-bottom: 1.5rem; }
        label { display: flex; flex-direction: column; font-size: 0.9rem; gap: 0.4rem; }
        input, button { padding: 0.55rem 0.75rem; border: 1px solid #ccc; border-radius: 6px; font-size: 0.95rem; }
        button { cursor: pointer; background: #1f6feb; color: #fff; border: none; transition: background 0.2s ease; }
        button:hover { background: #1159c3; }
        table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
        thead { background: #1f6feb; color: #fff; }
        th, td { padding: 0.65rem 0.75rem; border: 1px solid #e0e0e0; text-align: left; font-size: 0.95rem; }
        tbody tr:nth-child(odd) { background: rgba(0,0,0,0.03); }
        .status { margin-top: 1rem; font-size: 0.9rem; }
        .error { color: #d93025; }
        .success { color: #137333; }
        @media (max-width: 640px) {
            body { padding: 0 1rem; }
            form { grid-template-columns: 1fr; }
            table { display: block; overflow-x: auto; }
        }
        .pill { display: inline-flex; gap: 0.35rem; align-items: center; padding: 0.2rem 0.6rem; border-radius: 999px; background: rgba(31,111,235,0.12); color: #1f6feb; font-size: 0.8rem; }
    </style>
</head>
<body>
    <h1>Relatório diário de vendas e perdas</h1>
    <p>Esta página consulta a API <code>/stock_adm/client-sales-loss-history/by-day</code> e apresenta os resultados agregados por cost center e data.</p>
    <form id="filter-form">
        <label>
            Data inicial
            <input type="date" id="start-date" required>
        </label>
        <label>
            Data final
            <input type="date" id="end-date" required>
        </label>
        <label>
            ID do produto (opcional)
            <input type="number" id="product-id" min="1" placeholder="Ex.: 42">
        </label>
        <label>
            IDs de cost center (opcional, separados por vírgula)
            <input type="text" id="cost-centers" placeholder="Ex.: 3,12,45">
        </label>
        <button type="submit">Buscar</button>
    </form>

    <div id="status" class="status"></div>
    <table id="results-table" hidden>
        <thead>
            <tr>
                <th>Cost Center</th>
                <th>Produto</th>
                <th>Data</th>
                <th>Vendas (unidades)</th>
                <th>Perdas (unidades)</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        function formatDateToISO(date) {
            return date.toISOString().slice(0, 10);
        }

        const startInput = document.getElementById("start-date");
        const endInput = document.getElementById("end-date");
        const statusEl = document.getElementById("status");
        const tableEl = document.getElementById("results-table");
        const tbodyEl = tableEl.querySelector("tbody");

        // Preenche campos com últimos 7 dias
        const today = new Date();
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(today.getDate() - 7);
        endInput.value = formatDateToISO(today);
        startInput.value = formatDateToISO(sevenDaysAgo);

        document.getElementById("filter-form").addEventListener("submit", async (event) => {
            event.preventDefault();
            statusEl.textContent = "Buscando dados...";
            statusEl.className = "status";
            tableEl.hidden = true;
            tbodyEl.innerHTML = "";

            const params = new URLSearchParams();
            const startDate = startInput.value;
            const endDate = endInput.value;

            if (!startDate || !endDate) {
                statusEl.textContent = "Informe as datas inicial e final.";
                statusEl.classList.add("error");
                return;
            }

            params.set("start_date", startDate);
            params.set("end_date", endDate);

            const productIdValue = document.getElementById("product-id").value;
            if (productIdValue) {
                params.set("product_id", productIdValue);
            }

            const costCenterValue = document.getElementById("cost-centers").value;
            if (costCenterValue.trim()) {
                costCenterValue.split(",")
                    .map((value) => value.trim())
                    .filter((value) => value.length > 0)
                    .forEach((value) => params.append("cost_center_ids", value));
            }

            const apiUrl = `${window.location.origin}/stock_adm/client-sales-loss-history/by-day?${params.toString()}`;

            try {
                const response = await fetch(apiUrl, { credentials: "include" });
                if (!response.ok) {
                    const payload = await response.json().catch(() => null);
                    const message = payload?.error?.message || response.statusText || "Falha ao consultar a API.";
                    throw new Error(message);
                }

                const data = await response.json();
                if (!Array.isArray(data) || data.length === 0) {
                    statusEl.textContent = "Nenhum dado encontrado para os filtros informados.";
                    statusEl.classList.add("success");
                    return;
                }

                let rowsInserted = 0;

                data.forEach((group) => {
                    const results = Array.isArray(group.results) ? group.results : [];
                    if (results.length === 0) {
                        return;
                    }

                    results.forEach((entry) => {
                        const tr = document.createElement("tr");

                        const costCenterCell = document.createElement("td");
                        const nameLine = document.createElement("div");
                        nameLine.textContent = group.cost_center_name || "Sem nome";
                        const pill = document.createElement("span");
                        pill.className = "pill";
                        pill.textContent = group.cost_center_id;
                        costCenterCell.append(nameLine, pill);

                        const productCell = document.createElement("td");
                        const productName = entry.product_name || `Produto ${entry.product_id}`;
                        productCell.textContent = `${productName} (#${entry.product_id})`;

                        const dateCell = document.createElement("td");
                        dateCell.textContent = entry.date;

                        const soldCell = document.createElement("td");
                        soldCell.textContent = entry.sold_quantity ?? 0;

                        const lostCell = document.createElement("td");
                        lostCell.textContent = entry.lost_quantity ?? 0;

                        tr.append(costCenterCell, productCell, dateCell, soldCell, lostCell);
                        tbodyEl.appendChild(tr);
                        rowsInserted += 1;
                    });
                });

                if (rowsInserted === 0) {
                    statusEl.textContent = "Nenhum dado encontrado para os filtros informados.";
                    statusEl.classList.add("success");
                    return;
                }

                tableEl.hidden = false;
                statusEl.textContent = `Encontradas ${rowsInserted} linhas agregadas em ${data.length} cost centers.`;
                statusEl.classList.add("success");
            } catch (error) {
                console.error(error);
                statusEl.textContent = error.message || "Erro inesperado ao carregar os dados.";
                statusEl.classList.add("error");
            }
        });
    </script>
</body>
</html>"""
    return HTMLResponse(content=html)


@router.get("/sales/quantity/", include_in_schema=False)
@router.get(
    "/sales/quantity",
    response_model=SalesQuantityResponse,
    tags=["Sales"],
    summary="Total de vendas por período",
)
def get_sales_quantity(
    product_id: int = Query(..., description="ID do produto"),
    start_date: datetime = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="Data final (YYYY-MM-DD)"),
    cost_center_id: Optional[int] = Query(None, description="ID do cost center (opcional)"),
    retail_chain_id: Optional[int] = Query(None, description="ID da retail chain (opcional)"),
    db: Session = Depends(get_db),
):
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="end_date deve ser >= start_date")
    sd = start_date.date()
    ed = end_date.date()
    total = get_sales_quantity_controller(
        db,
        product_id=product_id,
        start_date=sd,
        end_date=ed,
        cost_center_id=cost_center_id,
        retail_chain_id=retail_chain_id,
    )
    return SalesQuantityResponse(
        product_id=product_id,
        start_date=sd,
        end_date=ed,
        total_sold=total,
        cost_center_id=cost_center_id,
        retail_chain_id=retail_chain_id,
    )


@router.patch("/stock-movements/sales/", include_in_schema=False)
@router.patch(
    "/stock-movements/sales",
    response_model=ClientSalesUpdateResult,
    tags=["Sales"],
    summary="Editar vendas do cliente por dia",
)
def update_client_sale_for_day(body: ClientSalesUpdateDTO, db: Session = Depends(get_db)):
    try:
        total = update_client_sale_for_day_controller(
            db,
            cost_center_id=body.cost_center_id,
            product_id=body.product_id,
            d=body.date,
            new_total_sold=body.total_sold,
        )
        return ClientSalesUpdateResult(
            cost_center_id=body.cost_center_id,
            product_id=body.product_id,
            date=body.date,
            total_sold=total,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
