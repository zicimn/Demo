from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING, Optional
from config.db import Base
from datetime import datetime

if TYPE_CHECKING:
    from .aimodel import Ai_Model


class Ai_Model_Cap(Base):
    __tablename__ = "ai_model_cap"

    __table_args__ = (
        UniqueConstraint("model_id", "cap_code", name="uk_model_cap"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    cap_code: Mapped[str] = mapped_column(String(64), nullable=False,comment="能力编码")
    cap_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="能力名称")
    support_status: Mapped[str] = mapped_column(String(32), nullable=False,comment="supported/unsupported/beta/non_thinking_only/partial")
    is_beta: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否 Beta")
    note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="补充说明")

    # 外键关系
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("ai_model.id"), nullable=False, comment="模型ID")
    model: Mapped["Ai_Model"] = relationship("Ai_Model", back_populates="capabilities")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Ai_Model_Capability(id={self.id}, code='{self.cap_code}')>"