from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from config.db import Base

if TYPE_CHECKING:
    from .aimodel import Ai_Model


class Ai_Model_Price(Base):
    __tablename__ = "ai_model_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("ai_model.id"), nullable=False, comment="模型ID")
    model: Mapped["Ai_Model"] = relationship("Ai_Model", back_populates="prices")

    price_type: Mapped[str] = mapped_column(String(255), nullable=False, comment="价格类型")
    price: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False, comment="价格")
    time_period: Mapped[Optional[str]] = mapped_column(String(255), comment="时间周期")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())