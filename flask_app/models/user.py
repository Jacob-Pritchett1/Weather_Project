from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
# from flask_app.models import post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "users"
    def __init__(self, data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.posts = []
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO user(first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(),NOW());
            """
        return connectToMySQL("users").query_db(query, data)
    @classmethod
    def get_one_by_id(cls, data):
        query = """SELECT * from users WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        one_user_object= cls(results[0])
        return one_user_object
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters. Please try again.")
            is_valid=False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters. Please try again.")
            is_valid=False
        if len(user['password']) < 8:
            flash("Passwords must be at least 8 characters long. Please try again.")
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("The passwords you have entered do not match. Please try again. ")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address. Please try again.")
            is_valid=False
        return is_valid
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result= connectToMySQL("users").query_db(query,data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])



