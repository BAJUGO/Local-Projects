import pytest
from fastapi.testclient import TestClient
from .main import app

@pytest.fixture
def client():
    return TestClient(app)



#! Важно обозвать файл именно так, + функцию именно так. Это позволяет нам не писать в каждом новом тестовом файле client = TestClient(app)
