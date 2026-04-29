from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    category_id: Optional[str] = None


class TaskUpdate(BaseModel):
    status: str  # "Todo" | "Ongoing" | "Done"


class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    status: Optional[str] = "Todo"
    category_id: Optional[str] = None
    created_at: Optional[str] = None