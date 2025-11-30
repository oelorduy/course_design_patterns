from flask import Flask
from flask_restful import Api
from endpoints.products import ProductsResource
from endpoints.categories import CategoriesResource
from endpoints.favorites import FavoritesResource
from endpoints.authentication import AuthenticationResource   
from utils.database_connection import DatabaseConnection

app = Flask(__name__)
api = Api(app)

db = DatabaseConnection("data/db.json")

api.add_resource(ProductsResource, "/products", "/products/<int:product_id>")
api.add_resource(CategoriesResource, "/categories", "/categories/<int:category_id>")
api.add_resource(FavoritesResource, "/favorites", "/favorites/<int:favorite_id>")

api.add_resource(AuthenticationResource, "/auth")

if __name__ == "__main__":
    app.run(debug=True)