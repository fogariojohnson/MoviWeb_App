from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()
Base = db.Model


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    user_movies = db.relationship('Movie', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='reviewed_user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, username='{self.username}', password='{self.password}', movies='{self.user_movies}, reviews={self.reviews}')"


class Movie(Base):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True)
    director = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster = db.Column(db.String)
    genre = db.Column(db.String)
    flag = db.Column(db.String)
    url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_reviews = db.relationship('Review', backref='reviewed_movie', lazy=True)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 10', name='check_valid_rating'),
    )

    def __repr__(self):
        return f"Movie(id={self.id}, title='{self.title}, director='{self.director}',  year={self.year}, rating={self.rating}, poster={self.poster}, genre={self.genre}, flag={self.flag}, url={self.url}, user_id={self.user_id}, user_reviews={self.user_reviews})"


class Review(Base):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 10', name='check_valid_rating'),
    )

    user = db.relationship('User', back_populates='reviews')
    movie = db.relationship('Movie', back_populates='user_reviews')

    def __repr__(self):
        return f"Review(review_id={self.review_id}, user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})"
