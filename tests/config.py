import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://gorest.co.in/public/v2")
GOREST_TOKEN = os.getenv("GOREST_TOKEN")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
API_LOG_LEVEL = os.getenv("API_LOG_LEVEL", "INFO")

