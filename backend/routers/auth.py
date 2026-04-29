from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from services.firebase import verify_token

router = APIRouter()


class TokenRequest(BaseModel):
    id_token: str


def get_current_user(authorization: str = Header(...)):
    """
    Dependency: Lấy user từ Bearer token trong header.
    Header format: Authorization: Bearer <id_token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    id_token = authorization.split(" ")[1]
    try:
        user = verify_token(id_token)
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/verify")
def verify(body: TokenRequest):
    """
    Xác thực Firebase ID token.
    Frontend gửi token sau khi đăng nhập Google, backend xác minh và trả về thông tin user.
    """
    try:
        user = verify_token(body.id_token)
        return {
            "uid": user["uid"],
            "email": user.get("email"),
            "name": user.get("name"),
            "picture": user.get("picture"),
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token không hợp lệ: {str(e)}")


@router.get("/me")
def me(authorization: str = Header(...)):
    """
    Lấy thông tin user hiện tại từ token.
    """
    user = get_current_user(authorization)
    return {
        "uid": user["uid"],
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture"),
    }