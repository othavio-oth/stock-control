from fastapi.testclient import TestClient
from app.api.main import app
import logging
import uuid

client = TestClient(app)

def test_user_full_flow():
    logger = logging.getLogger(__name__)
    logger.debug("Starting test_get_user")
    unique_id = uuid.uuid4().hex[:8]
    test_username = f"test_user_{unique_id}"
    test_email = f"test_{unique_id}@example.com"

    response_create = client.post(
        "/users/",
        json={
            "username": test_username,
            "email": test_email,
            "full_name": "Test User",
            "nickname": "Tester",
            "is_active": True,
            "is_superuser": False,
            "password": "testpassword"
        },
    )
    assert response_create.status_code == 200
    created_user = response_create.json()

    # Atualização do usuário
    new_username = f"updated_user_{unique_id}"
    new_email = f"updated_{unique_id}@example.com"
    response_update = client.put(
        f"/users/{created_user['id']}",
        json={
            "username": new_username,
            "email": new_email,
            "full_name": "Updated User",
            "nickname": "UpdatedTester",
            "is_active": True,
            "is_superuser": True,
        },
    )
    assert response_update.status_code == 200
    updated_user = response_update.json()
    assert updated_user["username"] == new_username
    assert updated_user["email"] == new_email

    # Deleção do usuário
    response_delete = client.delete(f"/users/{updated_user['id']}")
    assert response_delete.status_code == 200

    # Verifica que o usuário foi removido
    response_get = client.get(f"/users/1")
    assert response_get.status_code == 404

