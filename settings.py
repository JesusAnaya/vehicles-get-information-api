from pathlib import Path
from pydantic import BaseSettings


# Get the current directory
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    # SQLAlchemy
    database_url: str = "sqlite:///" + str(BASE_DIR / "app.db")

    database_test_url: str = "sqlite:///" + str(BASE_DIR / "test.db")

    # VPIC API
    vpic_host: str = "https://vpic.nhtsa.dot.gov"


settings = Settings()
