# database/get_url.py
import os
from urllib.parse import quote_plus

def get_url():
    """Generate database URL from environment variables."""
    user = quote_plus(os.getenv("DB_USER", ""))
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "postgres")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

if __name__ == "__main__":
    print(get_url())
