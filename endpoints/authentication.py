from flask_restful import Resource, reqparse
from services.auth_services import AuthService

class AuthenticationResource(Resource):

    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, help="Username is required")
        parser.add_argument("password", required=True, help="Password is required")
        data = parser.parse_args()

        token = AuthService.generate_token(
            data["username"],
            data["password"]
        )

        if token:
            return {"token": token}, 200
        
        return {"message": "Invalid credentials"}, 401