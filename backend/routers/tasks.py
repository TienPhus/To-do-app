from fastapi import APIRouter, HTTPException, Header
from schemas.task import TaskCreate, TaskUpdate
from services.firestore import get_tasks, create_task, update_task, delete_task
from services.firebase import verify_token
from typing import Optional

router = APIRouter()


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    id_token = authorization.split(" ")[1]
    try:
        return verify_token(id_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/")
def list_tasks(authorization: str = Header(...), category_id: Optional[str] = None):
    user = get_current_user(authorization)
    return {"tasks": get_tasks(user["uid"], category_id)}


@router.post("/")
def add_task(body: TaskCreate, authorization: str = Header(...)):
    user = get_current_user(authorization)
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="Tiêu đề không được rỗng")
    return create_task(user["uid"], body.title.strip(), body.category_id)


@router.patch("/{task_id}")
def update_task_status(task_id: str, body: TaskUpdate, authorization: str = Header(...)):
    user = get_current_user(authorization)
    updated = update_task(task_id, user["uid"], body.status)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task không tồn tại hoặc không có quyền")
    return updated


@router.delete("/{task_id}")
def remove_task(task_id: str, authorization: str = Header(...)):
    user = get_current_user(authorization)
    if not delete_task(task_id, user["uid"]):
        raise HTTPException(status_code=404, detail="Task không tồn tại hoặc không có quyền")
    return {"message": "Đã xóa task thành công"}