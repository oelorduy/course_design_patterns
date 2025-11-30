class ProductFactory:
    @staticmethod
    def create(data):
        # Normalizar nombre
        name = data.get("name", "").strip()

        # Precio (conversión y validación simple)
        price = float(data.get("price", 0))

        # Categoría
        category = data.get("category", "").strip()

        return {
            "name": name,
            "price": price,
            "category": category
        }