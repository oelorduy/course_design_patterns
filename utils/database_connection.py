import json
import os

class DatabaseConnection:
    _instance = None

    def __new__(cls, json_file_path="data/db.json"):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

            base_path = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.dirname(base_path)                   
            absolute_path = os.path.join(root_path, json_file_path)  

            cls._instance.json_file_path = absolute_path
            cls._instance.data = None

            cls._instance._load_data()

        return cls._instance


    def _load_data(self):
        if not os.path.exists(self.json_file_path):
            self.data = {"products": [], "categories": [], "favorites": []}
            self.save()
            return

        with open(self.json_file_path, "r") as file:
            self.data = json.load(file)


    def save(self):
        with open(self.json_file_path, "w") as file:
            json.dump(self.data, file, indent=4)


    # -------- PRODUCTS --------
    def get_products(self):
        return self.data.get("products", [])

    def add_product(self, new_product):
        self.data["products"].append(new_product)
        self.save()

    # -------- CATEGORIES --------
    def get_categories(self):
        return self.data.get("categories", [])

    def add_category(self, new_category):
        self.data["categories"].append(new_category)
        self.save()

    def remove_category(self, name):
        self.data["categories"] = [
            c for c in self.data["categories"] if c["name"] != name
        ]
        self.save()

    # -------- FAVORITES --------
    def get_favorites(self):
        return self.data.get("favorites", [])

    def add_favorite(self, new_favorite):
        self.data["favorites"].append(new_favorite)
        self.save()