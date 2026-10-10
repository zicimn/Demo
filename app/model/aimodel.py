from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING, Optional, List
from config.db import Base
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .provider import Provider
    from .aimodelcap import Ai_Model_Cap
    from .aimodelprice import Ai_Model_Price


class ThinkingSupport(str, Enum):
    """thinking_support 枚举值"""
    NONE = "none"
    NON_THINKING_ONLY = "non_thinking_only"
    THINKING_ONLY = "thinking_only"
    BOTH = "both"
    UNKNOWN = "unknown"


class Ai_Model(Base):
    __tablename__ = "ai_model"

    __table_args__ = (UniqueConstraint("provider_id", "model_slug", name="uk_provider_slug"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 标识字段
    model_slug: Mapped[str] = mapped_column(String(100), nullable=False, comment="模型标识/列名")
    display_name: Mapped[str] = mapped_column(String(150), nullable=False, comment="展示名")
    model_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="模型版本")
    model_family: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="模型系列")

    # 上下文长度
    context_length_raw: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, comment="上下文长度原文，如 1M")

    # 最大输出
    max_output_raw: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, comment="最大输出原文，如 最大 384K")

    # 思考模式
    thinking_support: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown",comment="思考模式支持")
    default_thinking_mode: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, comment="默认模式：non_thinking/thinking/unknown")
    thinking_note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="思考模式切换说明")

    # 限制与状态
    concurrency_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="并发限制")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active",comment="active/inactive/deprecated")

    # 文档与备注
    doc_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="模型文档地址")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="模型描述")
    
    # 外键关系
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("ai_provider.id"), nullable=False, comment="供应商ID")
    provider: Mapped["Provider"] = relationship("Provider", back_populates="ai_models")

    # 子表关系
    capabilities: Mapped[List["Ai_Model_Cap"]] = relationship("Ai_Model_Cap", back_populates="model", cascade="all, delete-orphan")
    prices: Mapped[List["Ai_Model_Price"]] = relationship("Ai_Model_Price", back_populates="model", cascade="all, delete-orphan")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Ai_Model(id={self.id}, slug='{self.model_slug}')>"