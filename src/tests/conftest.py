# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.pool import StaticPool
# from src.main import app

# from src.database import engine, SessionLocal
# import src.models as models
# from src.security import get_password_hash

# @pytest.fixture
# def client(session):
#     def get_session_override():
#         return session
    
#     with TestClient(app) as client:
#         app.dependency_overrides[get]