import pytest
from app.service.user_service import create_new_user, get_user_details
from app.schemas.user_schema import UserCreate

def test_create_new_user(db):
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="hashedpassword",
    )
    user = create_new_user(db, user_data)
    assert user.id is not None
    assert user.username == "newuser"

def test_get_user_details(db):
    user_data = UserCreate(
        username="detailuser",
        email="detailuser@example.com",
        password="hashedpassword",
    )
    user = create_new_user(db, user_data)
    retrieved_user = get_user_details(db, user.id)
    assert retrieved_user.id == user.id
    assert retrieved_user.username == "detailuser"
