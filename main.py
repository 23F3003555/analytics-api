
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_z81s7btyv7nje5vkoy0yyqug"
EMAIL = "23f3003555@ds.study.iitm.ac.in"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_totals = defaultdict(float)
    revenue = 0.0

    for event in request.events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] += event.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    return {
        "email": EMAIL,
        "total_events": len(request.events),
        "unique_users": len({event.user for event in request.events}),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }
