class CategoryRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.data.get("categories", [])

    def get_by_id(self, category_id):
        categories = self.db.data.get("categories", [])
        return next((c for c in categories if c["id"] == category_id), None)

    def add(self, category_data):
        categories = self.db.data.get("categories", [])
        categories.append(category_data)
        self.db.save()
        return category_data

    def update(self, category_id, new_data):
        categories = self.db.data.get("categories", [])
        for c in categories:
            if c["id"] == category_id:
                c.update(new_data)
                self.db.save()
                return c
        return None

    def delete_by_id(self, category_id):
        categories = self.db.data.get("categories", [])
        for c in categories:
            if c["id"] == category_id:
                categories.remove(c)
                self.db.save()
                return True
        return False

    def find_by_name(self, name):
        categories = self.db.get_categories()
        return next((c for c in categories if c["name"] == name), None)

    def delete_by_name(self, name):
        before = len(self.db.get_categories())
        self.db.remove_category(name)
        after = len(self.db.get_categories())
        return before != after