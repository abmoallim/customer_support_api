import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    POSTGRES_URL = os.getenv("POSTGRES_URL")

settings = Settings()
