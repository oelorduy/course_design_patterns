from flask import request
from flask_restful import Resource, reqparse
from utils.database_connection import DatabaseConnection
from services.auth_services import AuthService
from services.category_service import CategoryService
from repositories.category_repository import CategoryRepository


class CategoriesResource(Resource):
    def __init__(self):
        # Servicio de autenticación
        self.auth = AuthService()

        # Base de datos
        db = DatabaseConnection("db.json")
        db.connect()

        # Repository → Service
        repo = CategoryRepository(db)
        self.service = CategoryService(repo)

        # Parser para POST y PUT
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, required=True, help="Field 'name' is required")

    # =======================================================
    # GET /categories
    # GET /categories/<id>
    # GET /categories?name=Women
    # =======================================================
    def get(self, category_id=None):

        # Validación del token
        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        # GET /categories/<id>
        if category_id is not None:
            category = self.service.get_category_by_id(category_id)
            if category:
                return category, 200
            return {"error": "Category not found"}, 404

        # GET /categories
        categories = self.service.get_all_categories()

        # Filtro opcional ?name=Women
        filter_name = request.args.get("name")
        if filter_name:
            categories = [
                c for c in categories
                if c["name"].lower() == filter_name.lower()
            ]

        return categories, 200

    # =======================================================
    # POST /categories → crear
    # =======================================================
    def post(self):

        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        args = self.parser.parse_args()
        name = args["name"]

        new_category = {"name": name}
        created = self.service.create_category(new_category)

        return created, 201

    # =======================================================
    # PUT /categories/<id> → actualizar
    # =======================================================
    def put(self, category_id):

        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        args = self.parser.parse_args()
        updated = self.service.update_category(category_id, args)

        if updated:
            return updated, 200

        return {"error": "Category not found"}, 404

    # =======================================================
    # DELETE /categories/<id>
    # DELETE /categories?name=Women
    # DELETE /categories  (json: { "name": "Women" })
    # =======================================================
    def delete(self, category_id=None):

        # Validación del token
        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        # ---------- ELIMINAR POR ID ----------
        if category_id is not None:
            deleted = self.service.delete_category_by_id(category_id)
            if deleted:
                return {"message": "Category deleted by ID"}, 200
            return {"error": "Category not found"}, 404

        # ---------- ELIMINAR POR QUERY PARAM ----------
        query_name = request.args.get("name")
        if query_name:
            deleted = self.service.delete_category_by_name(query_name)
            if deleted:
                return {"message": "Category deleted by name"}, 200
            return {"error": "Category not found"}, 404

        # ---------- ELIMINAR POR JSON ----------
        data = request.get_json(silent=True) or {}
        json_name = data.get("name")

        if not json_name:
            return {"error": "You must provide JSON {\"name\": \"CategoryName\"}, ?name=CategoryName, or /<id>"}, 400

        deleted = self.service.delete_category_by_name(json_name)
        if deleted:
            return {"message": "Category deleted by name"}, 200

        return {"error": "Category not found"}, 404
"""
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from utils.database_connection import DatabaseConnection

def is_valid_token(token):
    return token == 'abcd1234'

class CategoriesResource(Resource):
    def __init__(self):

        self.db = DatabaseConnection('db.json')
        self.db.connect()

        self.categories_data = self.db.get_categories()
        self.parser = reqparse.RequestParser()

    def get(self, category_id=None):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        if category_id is not None:
            category = next((p for p in self.categories_data if p['id'] == category_id), None)
            if category is not None:
                return category
            else:
                return {'message': 'Category not found'}, 404
         
        return self.categories_data 

    def post(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        self.parser.add_argument('name', type=str, required=True, help='Name of the category')
 
        args = self.parser.parse_args()
        print("*****",args)
        new_category_name = args['name']
        if not new_category_name:
            return {'message': 'Category name is required'}, 400

        categories = self.categories_data
        if new_category_name in categories:
            return {'message': 'Category already exists'}, 400

        new_category = {
                'id': len(self.categories_data) + 1,
                'name': new_category_name
        }

        categories.append(new_category)
        self.categories_data = categories
        
        self.db.add_category(new_category)

        return {'message': 'Category added successfully'}, 201

    def delete(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        args = self.parser.parse_args()
        self.parser.add_argument('name', type=str, required=True, help='Name of the category')
        args = self.parser.parse_args()
        category_name = args['name']
 
        if not category_name:
            return {'message': 'Category name is required'}, 400

        category_to_remove = next((cat for cat in self.categories_data if cat["name"] == category_name), None)

        if category_to_remove is None:
            return {'message': 'Category not found'}, 404
        else:
            categories = [cat for cat in self.categories_data if cat["name"] != category_to_remove]
            self.categories_data = categories
            self.db.remove_category(category_name)

            return {'message': 'Category removed successfully'}, 200
           
"""

