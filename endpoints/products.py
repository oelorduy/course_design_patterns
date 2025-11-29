from flask import request
from flask_restful import Resource, reqparse
from services.auth_services import AuthService
from services.product_service import ProductService
from repositories.product_repository import ProductRepository
from utils.database_connection import DatabaseConnection

class ProductsResource(Resource):
    def __init__(self):
        self.auth = AuthService()

        db = DatabaseConnection("db.json")
        db.connect()

        repo = ProductRepository(db)
        self.service = ProductService(repo)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", required=True)
        self.parser.add_argument("category", required=True)
        self.parser.add_argument("price", type=float, required=False)

    # =======================================================
    #   GET /products
    #   GET /products/<id>
    #   GET /products?category=women
    # =======================================================
    def get(self, product_id=None):

        # VALIDACIÓN DEL TOKEN
        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        # GET /products/<id>
        if product_id is not None:
            product = self.service.get_product_by_id(product_id)
            if product:
                return product, 200
            return {"error": "Product not found"}, 404

        # GET /products
        products = self.service.get_all_products()

        # Filtro opcional ?category=women
        category = request.args.get("category")
        if category:
            products = [p for p in products if p.get("category") == category]

        return products, 200

    # =======================================================
    #   POST /products
    # =======================================================
    def post(self):

        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        args = self.parser.parse_args()

        new_product = self.service.create_product(args)
        return {"message": "Product added", "product": new_product}, 201