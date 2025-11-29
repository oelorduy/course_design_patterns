class FavoriteRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.data.get("favorites", [])

    def get_by_id(self, favorite_id):
        favorites = self.db.data.get("favorites", [])
        return next((c for c in favorites if c["id"] == favorite_id), None)

    def add(self, favorite_data):
        favorites = self.db.data.get("favorites", [])
        favorites.append(favorite_data)
        self.db.save()
        return favorite_data

    def update(self, favorite_id, new_data):
        favorites = self.db.data.get("favorites", [])
        for c in favorites:
            if c["id"] == favorite_id:
                c.update(new_data)
                self.db.save()
                return c
        return None

    def delete_by_id(self, favorite_id):
        favorites = self.db.data.get("favorites", [])
        for c in favorites:
            if c["id"] == favorite_id:
                favorites.remove(c)
                self.db.save()
                return True
        return False