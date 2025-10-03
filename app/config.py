import os
from dotenv import load_dotenv

load_dotenv()

class CoreCFG:
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", 8000))
    app_name: str = os.getenv("APP_NAME", "FastAPI Server")
    debug_env: str = os.getenv("APP_DEBUG", "false").lower()
    debug: bool = False if debug_env == "false" else True
    log_level: str = os.getenv("APP_LOG_LEVEL", "INFO")
    time_zone: str = os.getenv("APP_TIMEZONE", "Asia/Ho_Chi_Minh")

class DatabaseCFG:
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "db_name")
    db_url: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"