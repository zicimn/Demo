import logging
from typing import Any, Optional

from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    status_code = 500

    def __init__(self, msg: str, *, log: bool = True):
        self.msg = msg
        super().__init__(msg)

        if log:
            logger.warning("%s: %s", self.__class__.__name__, msg)


class NotFound(AppError):
    status_code = 404


def info(
    msg : str = "返回信息",
    code: int = 200,
    data: Optional[Any] = None,
    total: Optional[int] = None,
    detail: Optional[str] = None,
)->dict:
    return{
        "msg":msg,
        "code":code,
        "data":data,
        "total":total,
        "detail":detail,
    }


# 面向用户的简短提示：只按 HTTP 语义给通用文案，
# 具体错误（含 id、provider_code 等）放在 detail 里，避免 msg / detail 完全重复。
_ERROR_MSG_BY_STATUS: dict[int, str] = {
    400: "请求参数有误",
    401: "未认证或登录已过期",
    403: "没有访问权限",
    404: "请求的资源不存在或已停用",
    409: "请求的资源状态冲突",
    422: "请求参数校验失败",
    429: "请求过于频繁，请稍后再试",
    500: "服务器内部错误",
}


def fail(e: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=e.status_code,
        content=info(
            msg=_ERROR_MSG_BY_STATUS.get(e.status_code, "请求处理失败"),
            code=e.status_code,
            data=None,
            detail=e.msg,
        ),
    )


    