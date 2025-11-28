class ProductRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.data.get("products", [])

    def get_by_id(self, product_id):
        products = self.db.data.get("products", [])
        return next((p for p in products if p["id"] == product_id), None)

    def add(self, product_data):
        products = self.db.data.get("products", [])
        products.append(product_data)
        self.db.save()
        return product_data

    def update(self, product_id, new_data):
        products = self.db.data.get("products", [])
        for p in products:
            if p["id"] == product_id:
                p.update(new_data)
                self.db.save()
                return p
        return None

    def delete(self, product_id):
        products = self.db.data.get("products", [])
        for p in products:
            if p["id"] == product_id:
                products.remove(p)
                self.db.save()
                return True
        return False