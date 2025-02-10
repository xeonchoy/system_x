from flask_login import UserMixin
from database.db import get_user_by_username

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.password_hash = user_data['password']
        
    @staticmethod
    def get(username):
        user_data = get_user_by_username(username)
        if user_data:
            return User(user_data)
        return None
        
    def get_id(self):
        return str(self.username)
