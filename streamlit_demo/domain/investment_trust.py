from datetime import datetime
from pydantic import BaseModel, ConfigDict


class InvestmentTrust(BaseModel):
    id: int | None = None
    fund_name: str
    income_price: float
    income_percent: float
    evaluation_value: float
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(frozen=True)
