from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    user_movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', password='{self.password}',  movies='{self.movies}')"


class Movie(db.Model):
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


def __repr__(self):
    return f"Movie(id={self.id}, title='{self.title}, director='{self.director}',  year={self.year}, rating={self.rating} )"


# movies = db.session.query(Movie).all()
# for movie in movies:
#     print(movie.title)
