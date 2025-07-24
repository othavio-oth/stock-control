from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.middleware.db import get_db
import logging

from app.middleware.auth_handler import login
from app.middleware.permission import has_permission

from app.schemas.tickets_schemas.cost_center_schemas import CostCenterCreate, CostCenterUpdate, CostCenterResponse
from app.controller.tickets_controller.cost_center_controller import create_cost_center, list_cost_centers, edit_cost_center, delete_cost_center
from app.schemas.tickets_schemas.tickets_schemas import TicketCreate, TicketResponse, TicketProductCreate, TicketProductResponse
from app.controller.tickets_controller.tickets_controller import create_ticket, list_tickets, edit_ticket, delete_ticket, add_product_to_ticket_controller, remove_product_from_ticket_controller, get_products_for_ticket_controller, get_ticket_products_controller