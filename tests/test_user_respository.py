from app.repository.user_repository import create_user, get_user_by_email
from app.schemas.user_schema import UserCreate

def test_create_user(db):
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="hashedpassword",
        full_name="Test User",
        nickname="Tester",
    )
    user = create_user(db, user_data)
    assert user.id is not None
    assert user.username == "testuser"

def test_get_user_by_email(db):
    user_data = UserCreate(
        username="testuser2",
        email="testuser2@example.com",
        password="hashedpassword",
    )
    create_user(db, user_data)
    user = get_user_by_email(db, "testuser2@example.com")
    assert user is not None
    assert user.email == "testuser2@example.com"
