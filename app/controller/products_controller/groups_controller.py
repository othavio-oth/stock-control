from . import *

def list_groups(db):
    return GroupService.list_groups(db)

def create_group(group_data, db):
    return GroupService.create_group(db, group_data)

def edit_group(group_id, group_data, db):
    return GroupService.edit_group(db, group_id, group_data)

def delete_group(group_id, db):
    return GroupService.remove_group(db, group_id)