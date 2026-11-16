from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Transaction Analytics API")


class Transaction(BaseModel):
    id: int
    amount: float = Field(allow_inf_nan=False)
    category: str


class AnalyticsRequest(BaseModel):
    transactions: List[Transaction] = Field(min_length=1)


class AnalyticsSummary(BaseModel):
    total_revenue: float
    median_check: float


@app.post("/analytics/summary", response_model=AnalyticsSummary)
def get_analytics_summary(request: AnalyticsRequest) -> AnalyticsSummary:
    amounts = np.array([transaction.amount for transaction in request.transactions])
    return AnalyticsSummary(
        total_revenue=float(np.sum(amounts)),
        median_check=float(np.median(amounts)),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
