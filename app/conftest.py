import pytest


@pytest.fixture
def base_client(setup_database, client):
    return client

@pytest.fixture(autouse=True)
def setup_database(transactional_db):
    pass