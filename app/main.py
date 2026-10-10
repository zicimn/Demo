import os
from fastapi import FastAPI
from api.service import display_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# 允许前端跨域访问
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [o.strip() for o in cors_origins_str.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(display_router)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True,reload_excludes=["logs/*", "*.log", "__pycache__/*"])