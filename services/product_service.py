class ProductService:
    def __init__(self, repository):
        self.repository = repository

    def list_products(self, category=None):
        products = self.repository.get_all()
        if category:
            products = [p for p in products if p["category"] == category]
        return products

    def create_product(self, data):
        new_product = {
            "id": data["id"],
            "name": data["name"],
            "category": data["category"]
        }
        self.repository.add(new_product)
        return new_product