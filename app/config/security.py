import os
from pathlib import Path

from dotenv import load_dotenv

# 显式指定 .env 位置（app/.env），避免依赖 cwd 或 dotenv 的隐式向上查找
load_dotenv(Path(__file__).parents[1] / ".env")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

if not ASYNC_DATABASE_URL:
    raise ValueError("环境变量 ASYNC_DATABASE_URL 未设置，请检查 .env 文件")


