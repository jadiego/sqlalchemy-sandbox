import pytest
from sqlalchemy_sandbox.app import factory 

class TestApp:
    app = factory.create_test_app()
    assert app is not None
