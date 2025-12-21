from sqlalchemy.orm import Session

from app.models.user import Permission, RolePermission, Role, UserRole

from app.models.user import User
from app.models.product import  UnitMeasurement, UnitConversion,  Product, Category, RetailChain
from app.models.tickets import Ticket, TicketProduct, CostCenter
from app.schemas.users_schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.schemas.stock_schemas.stock_products_schemas import StockProductBase, StockProductCreate, StockProductUpdate, StockProductResponse
from app.schemas.stock_schemas.stock_products_schemas import StockProductHistoryBase, StockProductHistoryCreate, StockProductHistoryUpdate, StockProductHistoryResponse
from app.schemas.products_schemas.products_schemas import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from app.middleware.hash_password import hash_password