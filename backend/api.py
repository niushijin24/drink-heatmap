from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.db import get_redis
from redis.asyncio import Redis

router = APIRouter()

class JoinRequest(BaseModel):
    date: str  # Format: YYYY-MM-DD
    nickname: str

@router.get("/calendar/summary")
async def get_calendar_summary(r: Redis = Depends(get_redis)):
    """Get the heat map (count of participants) for all dates"""
    # Pattern to find all heat keys
    # Assuming key format: drink:heat:calendar (Hash)
    # Actually, using a Hash is better for retrieving all at once: 'drink:heat:calendar' field=date value=count
    
    data = await r.hgetall("drink:heat:calendar")
    # Convert string counts to integers
    return {date: int(count) for date, count in data.items()}

@router.post("/calendar/join")
async def join_date(req: JoinRequest, r: Redis = Depends(get_redis)):
    """User joins a date"""
    if not req.date or not req.nickname:
        raise HTTPException(status_code=400, detail="Date and nickname are required")

    # 1. 记录参与次数 (不再根据昵称去重,以支持连续点击增加火苗)
    await r.hincrby("drink:heat:calendar", req.date, 1)
    
    # 2. 可选:仍然记录参与者(虽然目前不显示)
    participants_key = f"drink:participants:{req.date}"
    await r.sadd(participants_key, req.nickname)

    return {"status": "joined", "message": f"Heat increased for {req.date}"}
