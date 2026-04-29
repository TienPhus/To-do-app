from services.firebase import get_db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP


def get_categories(user_id: str) -> list:
    db = get_db()
    docs = db.collection("categories").where("user_id", "==", user_id).stream()
    result = []
    for doc in docs:
        cat = doc.to_dict()
        cat["id"] = doc.id
        result.append(cat)
    return result


def create_category(user_id: str, name: str) -> dict:
    db = get_db()
    data = {"user_id": user_id, "name": name, "created_at": SERVER_TIMESTAMP}
    ref = db.collection("categories").add(data)
    return {"id": ref[1].id, "user_id": user_id, "name": name}


def delete_category(category_id: str, user_id: str) -> bool:
    db = get_db()
    ref = db.collection("categories").document(category_id)
    doc = ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != user_id:
        return False
    tasks = db.collection("tasks").where("category_id", "==", category_id).stream()
    for task in tasks:
        task.reference.delete()
    ref.delete()
    return True


def get_tasks(user_id: str, category_id: str = None) -> list:
    db = get_db()
    query = db.collection("tasks").where("user_id", "==", user_id)
    if category_id:
        query = query.where("category_id", "==", category_id)
    tasks = []
    for doc in query.stream():
        task = doc.to_dict()
        task["id"] = doc.id
        if task.get("created_at"):
            task["created_at"] = str(task["created_at"])
        tasks.append(task)
    return tasks


def create_task(user_id: str, title: str, category_id: str = None) -> dict:
    db = get_db()
    task_data = {
        "user_id": user_id,
        "title": title,
        "status": "Todo",
        "category_id": category_id,
        "created_at": SERVER_TIMESTAMP,
    }
    ref = db.collection("tasks").add(task_data)
    return {"id": ref[1].id, "user_id": user_id, "title": title,
            "status": "Todo", "category_id": category_id, "created_at": None}


def update_task(task_id: str, user_id: str, status: str) -> dict:
    db = get_db()
    ref = db.collection("tasks").document(task_id)
    doc = ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != user_id:
        return None

    ref.update({"status": status})

    updated = doc.to_dict()
    updated["id"] = task_id
    updated["status"] = status
    return updated


def delete_task(task_id: str, user_id: str) -> bool:
    db = get_db()
    ref = db.collection("tasks").document(task_id)
    doc = ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != user_id:
        return False
    ref.delete()
    return True