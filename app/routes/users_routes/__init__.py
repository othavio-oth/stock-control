from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.middleware.db import get_db
import logging

from app.middleware.auth_handler import login
from app.middleware.permission import has_permission

from app.schemas.users_schemas.permissions_schema import PermissionResponse, PermissionBase, PermissionRoleResponse, PermissionRequest, PermissionCreate, PermissionUpdate
from app.controller.users_controller.permission_controller import list_permissions, create_permission, edit_permission, remove_permission, assign_permission, unassign_permission, get_role_permissions, get_roles_from_permissions 

from app.schemas.users_schemas.roles_schema import RoleResponse, RoleBase, RoleUserResponse, RoleRequest
from app.controller.users_controller.roles_controller import list_roles, create_role, assign_role, get_role_user, edit_role, delete_role, delete_role_from_user

from app.schemas.users_schemas.user_schema import UserResponse, UserUpdate, UserCreate, UserResponseList
from app.controller.users_controller.user_controller import create_user, list_users, read_user, update_user, delete_user

from app.schemas.products_schemas.retail_chain_schemas import RetailChainBase, RetailChainResponse
from app.controller.products_controller.chain_controller import create_chain, list_chains,delete_chain, edit_chain

from app.schemas.products_schemas.unit_measurement_schemas import UnitMeasurementBase, UnitMeasurementResponse
from app.controller.products_controller.unit_measurement_controller import create_unit_measurement, list_unit_measurement, delete_unit_measurement, edit_unit_measurement

from app.schemas.products_schemas.unit_conversion_schema import ConversionBase, ConversionResponse, ConversionCreate, ConversionUpdate
from app.controller.products_controller.unit_conversion_controller import create_conversion, list_conversions, delete_conversion, edit_conversion

from app.schemas.products_schemas.category_schema import  Category, CategoryResponse, CategoryCreate, CategoryUpdate
from app.controller.products_controller.category_controller import create_category, list_categories, delete_category, edit_category


from app.schemas.products_schemas.products_schemas import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from app.controller.products_controller.product_controller import create_product, edit_product, delete_product

from app.repository.products import ProductPriceHistory
from app.schemas.products_schemas.product_price_schema import ProductPriceHistoryCreate



__all__= [
    "APIRouter",
    "Depends",
    "HTTPException",
    "status",
    "Body",
    "Dict",
    "List",
    "Optional",
    "Session",
    "get_db",
    "logging",
    
    "login",
    "has_permission",
    
    "PermissionResponse",
    "PermissionBase",
    "PermissionRoleResponse",
    "PermissionRequest",
    "PermissionCreate",
    "PermissionUpdate",
    
    
    
    "list_permissions",
    "create_permission",
    "edit_permission",
    "remove_permission",
    "assign_permission",
    "unassign_permission",
    "get_role_permissions",
    "get_roles_from_permissions",
    
    "RoleResponse",
    "RoleBase",
    "RoleUserResponse",
    "RoleRequest",
    "list_roles",
    "create_role",
    "assign_role",
    "get_role_user",
    "edit_role",
    "delete_role",
    "delete_role_from_user",
    
    "UserResponse",
    "UserUpdate",
    "UserCreate",
    "UserResponseList",
    "create_user",
    "list_users",
    "read_user",
    "update_user",
    "delete_user",
    
    "RetailChainBase",
    "RetailChainResponse",
    "create_chain",
    "list_chains",
    "edit_chain",
    "delete_chain",

    
    "UnitMeasurementBase",
    "UnitMeasurementResponse",
    "create_unit_measurement",
    "list_unit_measurement",
    "edit_unit_measurement",
    "delete_unit_measurement",
    
    "ConversionBase",
    "ConversionResponse",
    "ConversionCreate",
    "ConversionUpdate",
    "create_conversion",
    "list_conversions",
    "edit_conversion",
    "delete_conversion",

    
    "Category",
    "CategoryResponse",
    "CategoryCreate",
    "CategoryUpdate",
    "create_category",    
    "list_categories",
    "delete_category",
    "edit_category",
    
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    
    "create_product",
    "edit_product",
    "delete_product",
    
    "ProductPriceHistory",
    "ProductPriceHistoryCreate",

]