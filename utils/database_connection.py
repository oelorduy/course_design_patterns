import json

class DatabaseConnection:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = None

    def connect(self):
        try:
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = {"products": [], "categories": [], "favorites": []}
            self.save()

    # -----------------------
    #   SAVE FIX 
    # -----------------------
    def save(self):
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)

    # ========== PRODUCTS ==========
    def get_products(self):
        return self.data.get('products', [])

    def add_product(self, new_product):
        products = self.data.get('products', [])
        products.append(new_product)
        self.data['products'] = products
        self.save()

    # ========== CATEGORIES ==========
    def get_categories(self):
        return self.data.get('categories', [])

    def add_category(self, new_category):
        categories = self.data.get('categories', [])
        categories.append(new_category)
        self.data['categories'] = categories
        self.save()

    def remove_category(self, category_name):
        categories = self.data.get('categories', [])
        categories = [c for c in categories if c["name"] != category_name]
        self.data['categories'] = categories
        self.save()

    # ========== FAVORITES ==========
    def get_favorites(self):
        return self.data.get('favorites', [])

    def add_favorite(self, new_favorite):
        favorites = self.data.get('favorites', [])
        favorites.append(new_favorite)
        self.data['favorites'] = favorites
        self.save()