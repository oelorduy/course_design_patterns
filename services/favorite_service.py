from factories.favorite_factory import FavoriteFactory

class FavoriteService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_favorites(self):
        return self.repository.get_all()

    def get_favorite_by_id(self, favorite_id):
        return self.repository.get_by_id(favorite_id)

    def create_favorite(self, favorite_data):
        # 1. Obtener favoritos
        favorites = self.repository.get_all()

        # 2. Generar ID
        new_id = max([c["id"] for c in favorites], default=0) + 1

        # 3. Crear objeto usando Factory
        favorite = FavoriteFactory.create(favorite_data, new_id)

        # 4. Guardar
        return self.repository.add(favorite)

    def update_favorite(self, favorite_id, new_data):
        return self.repository.update(favorite_id, new_data)

    def delete_favorite_by_id(self, favorite_id):
        return self.repository.delete_by_id(favorite_id)
    
    def delete_favorite_by_name(self, name):
        favorites = self.repository.get_all()

        favorite = next(
            (f for f in favorites if f["name"].lower() == name.lower()),
            None
        )

        if not favorite:
            return False

        return self.repository.delete_by_id(favorite["id"])