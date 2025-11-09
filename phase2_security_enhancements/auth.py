import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

class AuthManager:
    """Authentication manager for secure mode"""

    def __init__(self, users_file: str = 'users.json'):
        self.users_file = users_file
        self._ensure_users_file()

    def _ensure_users_file(self):
        """Ensure users file exists"""
        if not os.path.exists(self.users_file):
            default_users = {
                'admin': {
                    'password_hash': self.hash_password('admin123'),
                    'is_admin': True,
                    'created_at': datetime.now().isoformat(),
                    'last_login': None
                }
            }
            import json
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def register_user(self, username: str, password: str, is_admin: bool = False) -> Dict:
        """Register a new user"""
        import json

        # Load existing users
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        # Check if user exists
        if username in users:
            raise ValueError("User already exists")

        # Create new user
        user_data = {
            'password_hash': self.hash_password(password),
            'is_admin': is_admin,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }

        users[username] = user_data

        # Save users
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return {
            'username': username,
            'is_admin': is_admin,
            'created_at': user_data['created_at']
        }

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data if valid"""
        import json

        if not os.path.exists(self.users_file):
            return None

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username not in users:
            return None

        user_data = users[username]

        # Verify password
        if not self.verify_password(password, user_data['password_hash']):
            return None

        # Update last login
        user_data['last_login'] = datetime.now().isoformat()
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return {
            'username': username,
            'is_admin': user_data['is_admin'],
            'created_at': user_data['created_at'],
            'last_login': user_data['last_login']
        }

    def generate_token(self, user_data: Dict) -> str:
        """Generate JWT token for user"""
        payload = {
            'username': user_data['username'],
            'is_admin': user_data['is_admin'],
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }

        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user_from_token(self, token: str) -> Optional[Dict]:
        """Get user data from token"""
        payload = self.verify_token(token)
        if not payload:
            return None

        return {
            'username': payload['username'],
            'is_admin': payload['is_admin']
        }

# Global auth manager instance
auth_manager = AuthManager()