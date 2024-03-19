import pytest
from app.users.dao import UserDAO


@pytest.mark.parametrize("id,email,existe", [
    (1, "artem@test.com", True),
    (3, "some@test.com", False)
])
async def test_find_user_by_id(id, existe, email):
    user = await UserDAO.find_by_id(id)

    if existe:
        assert user.id == 1
        assert user.email == email
    else:
        assert not user

    