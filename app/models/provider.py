from sqlalchemy import String, DateTime, Integer,TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING, Optional
from config.db import Base
from datetime import datetime

if TYPE_CHECKING:
    from .aimodel import Ai_Model


class Provider(Base):
    """模型供应商（对应 ai_provider 表）"""

    __tablename__ = "ai_provider"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider_code: Mapped[str] = mapped_column(String(50), nullable=False, comment="供应商标识，如 deepseek")
    provider_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="供应商名称，如 DeepSeek"
    )
    website_url: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="官网/文档地址"
    )
    description: Mapped[Optional[str]] = mapped_column(
        TEXT,nullable=True,comment="模型厂商介绍"
    )
    status: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, comment="1启用 0停用"
    )
    ico: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="供应商图标"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 反向关系
    ai_models: Mapped[list["Ai_Model"]] = relationship("Ai_Model", back_populates="provider")
    
    