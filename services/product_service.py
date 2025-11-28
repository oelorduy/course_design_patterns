class ProductService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_products(self):
        return self.repository.get_all()

    def get_product_by_id(self, product_id):
        return self.repository.get_by_id(product_id)

    def create_product(self, product_data):
        # -----------------------
        # 1. Obtener productos actuales
        # -----------------------
        products = self.repository.get_all()

        # -----------------------
        # 2. Generar ID automático
        # -----------------------
        new_id = max([p["id"] for p in products], default=0) + 1
        product_data["id"] = new_id

        # -----------------------
        # 3. Validación opcional
        # -----------------------
        if "name" not in product_data or "category" not in product_data:
            return {"error": "Missing 'name' or 'category' field"}, 400
        
        # -----------------------
        # 4. Guardar producto
        # -----------------------
        return self.repository.add(product_data)

    def update_product(self, product_id, new_data):
        return self.repository.update(product_id, new_data)

    def delete_product(self, product_id):
        return self.repository.delete(product_id)