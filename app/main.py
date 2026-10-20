import os
import sys
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import service_router

# 固定用 "main" 作为名字，避免 __name__ 在 python app/main.py 下变成 __main__
logger = logging.getLogger("main")

# 日志输出到终端（stdout）：各模块的 logger 都经 root 汇总到这里，
# 包括 err.AppError 抛出的 warning。uvicorn 自己的访问日志由其默认配置输出。
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

# 第三方库的 INFO 日志（如 httpx 的每次请求）太吵，只保留 WARNING 以上
# logging.getLogger("httpx").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("服务启动完成 | CORS=%s", ", ".join(cors_origins) or "(none)")
    for path in sorted({route.path for route in app.routes}):
        logger.info("已注册路由: %s", path)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """兜底：未预期的异常把完整堆栈打到终端，同时对外只回 500 不泄漏细节。
    业务异常（err.AppError）不在这里处理，由各路由自己 try/except 映射。"""
    logger.exception("未处理异常: %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})


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
app.include_router(service_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        reload=True, 
        log_level="debug",      # uvicorn 自己产生的日志也打到 DEBUG
        log_config=None,        # 关键：不用 uvicorn 自带的 logging 配置
        reload_excludes=["*.log", "__pycache__/*"]
    )