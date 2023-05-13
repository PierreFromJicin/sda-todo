from typing import Any
from typing import Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from database import engine
from main import api_router


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest_asyncio.fixture(scope="function")
async def app() -> Generator[FastAPI, Any, None]:
    from src.models.User import User
    from src.models.UserPassword import UserPassword
    from src.models.Todo import Todo

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

        _app = start_application()
        yield _app

        await conn.run_sync(SQLModel.metadata.drop_all)


# @pytest_asyncio.fixture(scope="function")
# async def db_session(app: FastAPI) -> Generator[async_session, Any, None]:
#     async with async_session() as session:
#         async with session.begin():
#             connection = engine.connect()
#             transaction = connection.begin()
#             yield session
#             session.close()
#             transaction.rollback()
#             connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI
) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client
