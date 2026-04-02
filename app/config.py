import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

if not DATABASE_URL or not SECRET_KEY:
    raise EnvironmentError("Убедитесь, что .env файл содержит DATABASE_URL и SECRET_KEY")