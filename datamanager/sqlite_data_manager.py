from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
from MoviWeb_App.datamanager.data_manager_interface import DataManagerInterface
from MoviWeb_App.datamanager.sql_model import db, Movie, User


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/myste/PycharmProjects/ProjectPart5/MoviWeb_App/storage/movies.sqlite'
# db = SQLAlchemy()


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        # self.db = SQLAlchemy()
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:/Users/myste/PycharmProjects/ProjectPart5/MoviWeb_App/storage/movies.sqlite'

    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.movies
        return []

    def add_user(self, name, username, password):
        new_user = User(name=name, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_data):
        movie = Movie.query.get(movie_id)
        if movie:
            for key, value in new_data.items():
                setattr(movie, key, value)
            db.session.commit()

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()