from flask import request
from flask_restful import Resource, reqparse
from utils.database_connection import DatabaseConnection
from services.auth_services import AuthService
from services.favorite_service import FavoriteService
from repositories.favorite_repository import FavoriteRepository


class FavoritesResource(Resource):
    def __init__(self):
        # Servicio de autenticación
        self.auth = AuthService()

        # Base de datos
        db = DatabaseConnection()
       
        # Repository → Service
        repo = FavoriteRepository(db)
        self.service = FavoriteService(repo)

        # Parser para POST y PUT
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, required=True, help="Field 'name' is required")


    # =======================================================
    # GET /favorites
    # GET /favorites/<id>
    # GET /favorites?name=xxxxxx
    # =======================================================
    def get(self, favorite_id=None):

        # Validación del token
        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        # GET /favorites/<id>
        if favorite_id is not None:
            favorite = self.service.get_favorite_by_id(favorite_id)
            if favorite:
                return favorite, 200
            return {"error": "Favorite not found"}, 404

        # GET /favorites
        favorites = self.service.get_all_favorites()

        # Filtro opcional ?name=xxxxx
        filter_name = request.args.get("name")
        if filter_name:
            favorites = [
                c for c in favorites
                if c["name"].lower() == filter_name.lower()
            ]

        return favorites, 200


    # =======================================================
    # POST /favorites
    # =======================================================
    def post(self):

        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        args = self.parser.parse_args()

        new_favorite = {
            "name": args["name"]
        }

        created = self.service.create_favorite(new_favorite)

        return created, 201


    # =======================================================
    # PUT /favorites/<id>
    # =======================================================
    def put(self, favorite_id):

        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        args = self.parser.parse_args()

        updated = self.service.update_favorite(favorite_id, args)

        if updated:
            return updated, 200

        return {"error": "Favorite not found"}, 404


    # =======================================================
    # DELETE /favorites/<id>
    # DELETE /favorites  → body JSON: { "name": "xxx" }
    # =======================================================
    def delete(self, favorite_id=None):

        token = request.headers.get("Authorization")
        if not self.auth.is_valid(token):
            return {"error": "Unauthorized"}, 401

        # -------- ELIMINAR POR ID --------
        if favorite_id is not None:
            deleted = self.service.delete_favorite_by_id(favorite_id)
            if deleted:
                return {"message": "Favorite deleted by ID"}, 200
            return {"error": "Favorite not found"}, 404

        # -------- ELIMINAR POR BODY JSON --------
        data = request.get_json()
        if not data or "name" not in data:
            return {"error": "You must provide a JSON with { 'name': '...' } or /<id>"}, 400

        deleted = self.service.delete_favorite_by_name(data["name"])

        if deleted:
            return {"message": "Favorite deleted by name"}, 200

        return {"error": "Favorite not found"}, 404