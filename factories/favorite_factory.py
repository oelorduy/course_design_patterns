class FavoriteFactory:
    @staticmethod
    def create(data: dict, new_id: int):
       
        name = data.get("name", "").strip()

        return {
            "id": new_id,
            "name": name
        }