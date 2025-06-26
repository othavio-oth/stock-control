from app.repository.products.groups_repository import create_group, delete_group, get_all_groups, get_group_by_id, update_group
from sqlalchemy.orm import Session
from app.schemas.products_schemas.group_schemas import GroupBase, GroupResponse
from app.models.groups import Group

class GroupService:
    @staticmethod
    def list_groups(db):
        return get_all_groups(db)

    @staticmethod
    def create_group(db, group_data):
        existing_group = db.query(Group).filter(Group.name == group_data.name).first()
        if existing_group:
            raise ValueError("Group com este name já existe.")
        return create_group(db, group_data)

    @staticmethod
    def edit_group(db, group_id, group_data):
        if not get_group_by_id(db, group_id):
            raise ValueError("Group não encontrado.")
        return update_group(db, group_id, group_data)

    @staticmethod
    def remove_group(db, group_id):
        if not get_group_by_id(db, group_id):
            raise ValueError("Group não encontrado.")
        return delete_group(db, group_id)