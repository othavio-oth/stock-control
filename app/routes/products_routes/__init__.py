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

from app.schemas.products_schemas.group_schemas import GroupBase, GroupResponse
from app.controller.products_controller.groups_controller import create_group, list_groups, delete_group, edit_group

from app.schemas.products_schemas.unit_measurement_schemas import UnitMeasurementBase, UnitMeasurementResponse
from app.controller.products_controller.unit_measurement_controller import create_unit_measurement, list_unit_measurement, delete_unit_measurement, edit_unit_measurement

from app.schemas.products_schemas.unit_conversion_schema import ConversionBase, ConversionResponse, ConversionCreate, ConversionUpdate
from app.controller.products_controller.unit_conversion_controller import create_conversion, list_conversions, delete_conversion, edit_conversion, get_conversion_by_id

from app.schemas.products_schemas.type_registration_schema import TypeRegistrationBase, TypeRegistrationResponse, TypeRegistrationCreate, TypeRegistrationUpdate
from app.controller.products_controller.type_registration_controller import create_type_registration, delete_type_registration, edit_type_registration, list_type_registrations

from app.schemas.products_schemas.products_schemas import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from app.controller.products_controller.product_controller import create_product, list_products, edit_product, delete_product

from app.schemas.products_schemas.cost_taxation_schemas import CostTaxationBase, CostTaxationResponse, CostTaxationCreate, CostTaxationUpdate
from app.controller.products_controller.cost_taxation_controller import create_cost_taxation, list_cost_taxations, edit_cost_taxation, delete_cost_taxation

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
    
    "GroupBase",
    "GroupResponse",
    "create_group",
    "list_groups",
    "edit_group",
    "delete_group",
    
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
    "get_conversion_by_id",
    "delete_conversion",
    
    "TypeRegistrationBase",
    "TypeRegistrationResponse",
    "TypeRegistrationCreate",
    "TypeRegistrationUpdate",
    "create_type_registration",
    "delete_type_registration",
    "edit_type_registration",
    "list_type_registrations",
    
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    
    "create_product",
    "list_products",
    "edit_product",
    "delete_product",
    
    "CostTaxationBase",
    "CostTaxationResponse",
    "CostTaxationCreate",
    "CostTaxationUpdate",
    "create_cost_taxation",
    "list_cost_taxations",
    "edit_cost_taxation",
    "delete_cost_taxation",
]