import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Khởi tạo Firebase Admin SDK (chỉ khởi tạo 1 lần)
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def verify_token(id_token: str) -> dict:
    """
    Xác thực Firebase ID token từ frontend.
    Trả về thông tin user nếu hợp lệ, raise Exception nếu không hợp lệ.
    """
    decoded = auth.verify_id_token(id_token)
    return decoded


def get_db():
    return db