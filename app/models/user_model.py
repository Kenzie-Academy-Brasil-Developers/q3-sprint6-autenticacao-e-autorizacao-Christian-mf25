from sqlalchemy import Column, Integer, String
from app.configs.database import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class UsersModel(db.Model):
    
    name: str
    last_name: str
    email: str

    keys = ["name", "last_name", "email", "password"]

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    last_name = Column(String(511), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)
    api_key = Column(String(511), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not accessible")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @classmethod
    def right_key(cls, key_to_check):
        wrong_keys = list(key_to_check - cls.keys)
        if wrong_keys:
            raise KeyError({"wrong_keys": wrong_keys})
    