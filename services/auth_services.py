import hashlib
import time
import base64

class AuthService:

    @staticmethod
    def generate_token(username, password):
        
        if username != "admin" or password != "1234":
            return None

        raw = f"{username}:{password}:{time.time()}"
        hashed = hashlib.sha256(raw.encode()).hexdigest()

        token = base64.urlsafe_b64encode(hashed.encode()).decode()
        return token


    @staticmethod
    def is_valid(token):
        
        if not token or len(token) < 20:
            return False
        
        try:
            base64.urlsafe_b64decode(token.encode())
            return True
        except Exception:
            return False