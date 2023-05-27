from sqlalchemy.orm import Session
from settings import settings
from db.base import Base
from tests.common import SessionForTesting
import pytest
import sqlalchemy

#
# This fixture is used to create a new database for each test function.
# The database is dropped after the test function is finished.
#
@pytest.fixture(scope="function")
def db_engine():
    url = settings.database_test_url
    engine = sqlalchemy.create_engine(url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()


#
# This fixture is used to create a new database session for each test function.
# The session is closed after the test function is finished.
#
@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
    SessionForTesting.configure(bind=db_engine)
    db_session = SessionForTesting()
    try:
        yield db_session
    finally:
        db_session.close()
        SessionForTesting.remove()


