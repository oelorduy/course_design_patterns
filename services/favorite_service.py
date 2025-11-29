class FavoriteService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_favorites(self):
        return self.repository.get_all()

    def get_favorite_by_id(self, favorite_id):
        return self.repository.get_by_id(favorite_id)

    def create_favorite(self, favorite_data):
        favorites = self.repository.get_all()
        new_id = max([c["id"] for c in favorites], default=0) + 1
        favorite_data["id"] = new_id
        return self.repository.add(favorite_data)

    def update_favorite(self, favorite_id, new_data):
        return self.repository.update(favorite_id, new_data)

    def delete_favorite_by_id(self, favorite_id):
        return self.repository.delete_by_id(favorite_id)  