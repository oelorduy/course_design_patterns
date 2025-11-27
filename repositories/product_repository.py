class ProductRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.read("products")

    def add(self, product):
        db_data = self.db.read("products")
        db_data.append(product)
        self.db.write("products", db_data)