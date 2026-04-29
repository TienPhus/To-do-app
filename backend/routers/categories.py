from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from services.firestore import get_categories, create_category, delete_category
from services.firebase import verify_token

router = APIRouter()


class CategoryCreate(BaseModel):
    name: str


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    id_token = authorization.split(" ")[1]
    try:
        return verify_token(id_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/")
def list_categories(authorization: str = Header(...)):
    user = get_current_user(authorization)
    return {"categories": get_categories(user["uid"])}


@router.post("/")
def add_category(body: CategoryCreate, authorization: str = Header(...)):
    user = get_current_user(authorization)
    if not body.name.strip():
        raise HTTPException(status_code=400, detail="Tên danh mục không được rỗng")
    return create_category(user["uid"], body.name.strip())


@router.delete("/{category_id}")
def remove_category(category_id: str, authorization: str = Header(...)):
    user = get_current_user(authorization)
    success = delete_category(category_id, user["uid"])
    if not success:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại hoặc không có quyền")
    return {"message": "Đã xóa danh mục và toàn bộ tasks bên trong"}