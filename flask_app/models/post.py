from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Post:
    DB = "users"
    def __init__(self,data):
        self.id= data['id']
        self.text=data['text']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id= None
    @classmethod # Create a new post in the DB
    def create_post(cls, data):
        query = """ INSERT INTO post(text, created_at, updated_at, user_id)
        VALUES (%(text)s, NOW(), NOW(), %(user_id)s);"""
        return connectToMySQL('users').query_db(query, data)
    @staticmethod 
    def validate_post(post):
        is_valid=True
        if len(post["text"]) < 1:
            flash("Your post must have content. Please try again.")
            is_valid = False
        return is_valid
    @classmethod 
    def get_one(cls, id):
        query = "SELECT * from post WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, {"id":id})
        one_post = []
        for row in results:
            one_post.append(cls(row))
        return one_post

    @classmethod # get all posts
    def get_all_posts(cls):
        query= "SELECT * from post"
        results = connectToMySQL(cls.DB).query_db(query)
        all_posts = []
        for row in results:
            all_posts.append(cls(row))
        return all_posts
    @classmethod
    def edit_post(cls, data):
        query = """ UPDATE post SET text=%(text)s WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM post WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query,data)
    @classmethod
    def users_posts(cls, data):
        query= "SELECT * from user LEFT JOIN post ON post.user_id = user.id WHERE user.id = %(id)s;"
        results= connectToMySQL('users').query_db(query, data)
        print(results)
        user_ = User.User(results[0])
        for row_from_db in results:
            post_data = {
            "id": row_from_db['post.id'],
            "text": row_from_db['text'],
            "created_at": row_from_db['post.created_at'],
            "updated_at": row_from_db['post.updated_at']
        }
        user_.post.append(cls(post_data))
        return user_
    @classmethod
    def post_users(cls):
        query= "SELECT * from post LEFT JOIN user ON user.id = user_id;"
        results= connectToMySQL('users').query_db(query)
        print(results)
        posts = []
        for row_from_db in results:
            post=cls(row_from_db)
            identified_user = { 
                "id":row_from_db["user.id"],
                "first_name":row_from_db["first_name"],
                "last_name":row_from_db["last_name"],
                "email":row_from_db["email"],
                "password":row_from_db["password"],
                "created_at":row_from_db["user.created_at"],
                "updated_at":row_from_db["user.updated_at"]
            }
            post = cls(row_from_db)
            post.user = User(identified_user)
            posts.append(post)
        return posts


