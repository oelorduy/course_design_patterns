
from flask import request
from flask_restful import Resource
from services.auth_services import AuthService


class AuthenticationResource(Resource):
    def __init__(self):
        self.auth_service = AuthService()

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        # Lógica simple de login
        if username == 'student' and password == 'desingp':
            token = "abcd1234"   # Debe coincidir con AuthService
            return {"token": token}, 200
        else:
            return {"message": "unauthorized"}, 401