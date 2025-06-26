# General Imports 
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import Config
from app.middleware.db import get_db
import logging

# Permissions Imports
from app.service.users_service.permission_service import PermissionService
from app.schemas.users_schemas.permissions_schema import PermissionBase, PermissionResponse

# Roles Imports
from app.service.users_service.roles_service import RolesService
from app.schemas.users_schemas.roles_schema import RoleBase, RoleResponse

# User Imports
from app.service.users_service.user_service import create_new_user, get_user_details, modify_user, remove_user, service_list_users
from app.schemas.users_schemas.user_schema import UserCreate, UserUpdate

# Groups Imports
from app.service.products_service.groups_service import GroupService
from app.schemas.products_schemas.group_schemas import GroupBase, GroupResponse

# Unit Measurements Imports
from app.service.products_service.unit_measurement_service import UnitMeasurementService
from app.schemas.products_schemas.unit_measurement_schemas import UnitMeasurementBase, UnitMeasurementResponse

# Conversion Imports
from app.service.products_service.unit_conversion_service import ConversionService
from app.schemas.products_schemas.unit_conversion_schema import ConversionBase, ConversionResponse

# Type Registration Imports
from app.service.products_service.type_registration_service import TypeRegistrationService
from app.schemas.products_schemas.type_registration_schema import TypeRegistrationBase, TypeRegistrationResponse

# Products Imports
from app.service.products_service.products_service import ProductService
from app.schemas.products_schemas.products_schemas import ProductBase, ProductCreate, ProductUpdate, ProductResponse

# Cost Taxation Imports
from app.service.products_service.cost_taxation_service import CostTaxationService
from app.schemas.products_schemas.cost_taxation_schemas import CostTaxationBase, CostTaxationResponse, CostTaxationCreate, CostTaxationUpdate

__all__ = [
    "Depends",
    "HTTPException",
    "status",
    "Session",
    "Config",
    "logging",
    
    "PermissionService",
    "PermissionBase",
    "PermissionResponse",
    
    "RolesService",
    "RoleBase",
    "RoleResponse",
    
    "create_new_user",
    "get_user_details",
    "modify_user",
    "remove_user",
    "service_list_users",
    "get_db",
    "UserCreate",
    "UserUpdate",
    
    "GroupService",
    "GroupBase",
    "GroupResponse",
    
    "UnitMeasurementService",
    "UnitMeasurementBase",
    "UnitMeasurementResponse",
    
    "ConversionService",
    "ConversionBase",
    "ConversionResponse",
    
    "TypeRegistrationService",
    "TypeRegistrationBase",
    "TypeRegistrationResponse",
    
    "ProductBase",
    "ProductService",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    
    "CostTaxationService",
    "CostTaxationBase",
    "CostTaxationResponse",
    "CostTaxationCreate",
    "CostTaxationUpdate",
]