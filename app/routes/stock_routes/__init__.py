from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.middleware.db import get_db
from app.middleware.auth_handler import get_current_user
from app.middleware.permission import has_permission
import logging

from app.middleware.auth_handler import login

from app.schemas.tickets_schemas.cost_center_schemas import CostCenterCreate, CostCenterUpdate, CostCenterResponse
from app.controller.tickets_controller.cost_center_controller import create_cost_center, list_cost_centers, edit_cost_center, delete_cost_center
from app.schemas.stock_schemas.stock_products_schemas import StockProductBase, StockProductResponse, StockProductHistoryBase, StockProductHistoryResponse, StockProductCreate, StockProductUpdate, StockProductHistoryCreate, StockProductHistoryUpdate
