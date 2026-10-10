import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

if not ASYNC_DATABASE_URL:
    raise ValueError("环境变量 ASYNC_DATABASE_URL 未设置，请检查 .env 文件")


