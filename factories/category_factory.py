from datetime import datetime

class CategoryFactory:
    @staticmethod
    def create(payload: dict, new_id: int) -> dict:
        name = payload.get("name")
        if isinstance(name, str):
            name = name.strip()
        return {
            "id": new_id,
            "name": name,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }