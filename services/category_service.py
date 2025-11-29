from factories.category_factory import CategoryFactory
class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_categories(self):
        return self.repository.get_all()

    def get_category_by_id(self, category_id):
        return self.repository.get_by_id(category_id)

    def create_category(self, category_data):
        # 1) Obtener categorías actuales
        categories = self.repository.get_all()

        # 2) Generar ID automático
        new_id = max([p["id"] for p in categories], default=0) + 1

        # 3) Validar entrada mínima
        if "name" not in category_data or not str(category_data.get("name", "")).strip():
            return {"error": "Missing 'name' field"}, 400

        # 4) Usar la factory para construir el objeto final
        category_obj = CategoryFactory.create(category_data, new_id)

        # 5) Persistir
        saved = self.repository.add(category_obj)
        return saved

    def update_category(self, category_id, new_data):
        return self.repository.update(category_id, new_data)

    def delete_category_by_id(self, category_id):
        return self.repository.delete_by_id(category_id)

    def delete_category_by_name(self, name):
        return self.repository.delete_by_name(name)