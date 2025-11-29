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




"""
from flask_restful import Resource, reqparse
import json
from flask import request
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'

class ProductsResource(Resource):
    def __init__(self):
       
        self.db = DatabaseConnection('db.json')
        self.db.connect()

        self.products = self.db.get_products()
        self.parser = reqparse.RequestParser()
        
    def get(self, product_id=None):
        args = self.parser.parse_args()
        token = request.headers.get('Authorization')
        category_filter = request.args.get('category')
      
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401

        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        if category_filter:
            filtered_products = [p for p in self.products if p['category'].lower() == category_filter.lower()]
            return filtered_products 
        
        if product_id is not None:
            product = next((p for p in self.products if p['id'] == product_id), None)
            if product is not None:
                return product
            else:
                return {'message': 'Product not found'}, 404
              
        return self.products

    def post(self):
        token = request.headers.get('Authorization')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the product')
        parser.add_argument('category', type=str, required=True, help='Category of the product')
        parser.add_argument('price', type=float, required=True, help='Price of the product')

        args = parser.parse_args()
        new_product = {
            'id': len(self.products) + 1,
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }

        self.products.append(new_product)
        self.db.add_product(new_product)
        return {'mensaje': 'Product added', 'product': new_product}, 201

"""




