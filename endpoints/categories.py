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
        db = DatabaseConnection()
       
        # Repository → Service
        repo = CategoryRepository(db)
        self.service = CategoryService(repo)

        # Parser para POST y PUT
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, required=True, help="Field 'name' is required")

    # =======================================================
    # GET /categories
    # GET /categories/<id>
    # GET /categories?name=xxxxxx
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