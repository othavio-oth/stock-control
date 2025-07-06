# General Imports 
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import Config
from app.middleware.db import get_db
import logging

# Stock imports
from app.service.stock_service.stock_product_service import StockProductService, StockProductHistoryService
from app.schemas.stock_schemas.stock_products_schemas import StockProductBase, StockProductResponse, StockProductHistoryBase, StockProductHistoryResponse

# Tickets imports
from app.service.tickets_service.tickets_service import TicketService
from app.schemas.tickets_schemas.tickets_schemas import TicketBase, TicketResponse