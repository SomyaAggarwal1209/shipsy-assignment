import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app, db

@pytest.fixture(scope="module")
def test_client():
    # Configure app for testing
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    # Use in-memory DB for speed and isolation
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    # create the test client
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()