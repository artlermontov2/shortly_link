from datetime import datetime

from httpx import AsyncClient

from app.reduction.dao import ReductionDAO


async def test_add(ac: AsyncClient):
    result = await ReductionDAO.add(
            long_url="https://aminalaee.dev/sqladmin/working_with_files/",
            user_id=1,
            token="uREknik",
            created_at=datetime.strptime("2024-02-12", "%Y-%m-%d"),
            expiry_at=datetime.strptime("2024-03-13", "%Y-%m-%d")
    )

    assert result.user_id == 1
    assert isinstance(result.token, str)

    token = await ReductionDAO.find_token("https://aminalaee.dev/sqladmin/working_with_files/")
    assert token is not None

    url = await ReductionDAO.find_original_url("uREknik")
    assert url is not None
