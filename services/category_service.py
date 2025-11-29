class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_categories(self):
        return self.repository.get_all()

    def get_category_by_id(self, category_id):
        return self.repository.get_by_id(category_id)

    def create_category(self, category_data):
        categories = self.repository.get_all()
        new_id = max([c["id"] for c in categories], default=0) + 1
        category_data["id"] = new_id
        return self.repository.add(category_data)

    def update_category(self, category_id, new_data):
        return self.repository.update(category_id, new_data)

    def delete_category_by_id(self, category_id):
        return self.repository.delete_by_id(category_id)

    def delete_category_by_name(self, name):
        return self.repository.delete_by_name(name)