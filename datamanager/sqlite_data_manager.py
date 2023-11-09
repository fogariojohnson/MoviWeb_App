from .sql_model import db, User, Movie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .data_manager_interface import DataManagerInterface
import imdb
import requests


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        # Create an SQLAlchemy engine
        self.engine = create_engine(f'sqlite:///{db_file_name}')

        # Create a session factory using the engine
        session = sessionmaker(bind=self.engine)

        # Initialize a session
        self.session = session()

        self.country_dict = {}

    def get_all_users(self):
        try:
            users = self.session.query(User).all()
            return users
        except Exception as e:
            print(f"Error in get_all_users: {str(e)}")
            return []

    @staticmethod
    def add_user(name, username, password):
        new_user = User(name=name, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    def genre_maker(self, genre):
        """ Creates a genre image of the movie

        Args:
            genre(str): Emoticon to display

        Returns:
            character(str): A link to the character image
        """
        api_key = "RRhRnIM0DDVn6BbmwULBzQ==n9DVxWtNtkN2nwH5"
        api_url = 'https://api.api-ninjas.com/v1/emoji?name={}'.format(genre)
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        list_options = response.json()
        for char in list_options:
            character = char["image"]
        return character

    def get_country_code(self):
        """ Creates the country code.

        Returns:
            country_dict(dict): A dictionary of countries and its code
        """
        api_key_holiday = "a47a88cb-3005-44d5-99d8-81710c7975cb"
        country_list = requests.get(f"https://holidayapi.com/v1/countries?pretty&key={api_key_holiday}")
        res = country_list.json()
        countries = res["countries"]
        dictionary = {}
        for country in countries:
            country_entry = country['name']
            code_entry = country['code']
            dictionary[country_entry] = code_entry
        self.country_dict = dictionary
        return self.country_dict

    def movie_data(self, title):
        # Create an IMDb object
        ia = imdb.IMDb()

        # Search for a movie
        movies = ia.search_movie(title)

        # Get the IMDb ID of the first movie in the search results
        movie_id = movies[0].getID()

        # Retrieve the complete movie information
        movie = ia.get_movie(movie_id)

        # Retrieve country of origin
        countries_of_origin = movie.get('countries')
        if countries_of_origin:
            country = countries_of_origin[0]
        movie_country_code = self.get_country_code()
        country_origin = movie_country_code[country]
        flag = f'https://flagsapi.com/{country_origin}/shiny/64.png'

        # Retrieve the director(s)
        directors = movie.get('director')
        if directors:
            director_names = [director.get('name') for director in directors]

        # Retrieve the genre
        movie_genre = ', '.join(movie['genres'])
        genres = movie_genre.split(', ')
        first_genre = genres[0]

        dict_of_genre_emoticons = {
            "Horror": "vampire",
            "Action": "bomb",
            "Western": "cowboy hat face",
            "Adventure": "person climbing",
            "Animation": "mage",
            "Comedy": "clown face",
            "Crime": "kitchen knife",
            "Drama": "loudly crying face",
            "Fantasy": "fairy",
            "Mystery": "detective",
            "Romance": "kiss",
            "Science Fiction": "alien",
            "Thriller": "ogre",
            "War": "crossed swords"
        }
        for key in dict_of_genre_emoticons.keys():
            if key == first_genre:
                genre = dict_of_genre_emoticons[key]
                movie_genre = self.genre_maker(genre)

        # Retrieve the poster URL (JPEG image)
        poster_url = movie.get('cover url')

        # Retrieve the IMDb URL
        imdb_url = movie.get('full-size cover url')

        new_movie = {
            "title": movie['title'],
            "director": ', '.join(director_names),
            "year": movie['year'],
            "rating": movie['rating'],
            "poster": poster_url,
            "genre": movie_genre,
            "flag": flag,
            "url": imdb_url
        }

        return new_movie

    def add_movie(self, user_id, title):
        try:
            existing_movie = self.session.query(Movie).filter_by(title=title).first()

            if existing_movie:
                print("Movie already exists. You might want to handle updating instead of adding.")
                # Handle updating or return existing_movie

            else:
                user = self.session.query(User).filter_by(id=user_id).first()
                if user:
                    movie_data_dict = self.movie_data(title)
                    print(movie_data_dict)
                    new_movie = Movie(
                        title=movie_data_dict['title'],
                        director=movie_data_dict['director'],
                        year=movie_data_dict['year'],
                        rating=movie_data_dict['rating'],
                        poster=movie_data_dict['poster'],
                        genre=movie_data_dict['genre'],
                        flag=movie_data_dict['flag'],
                        url=movie_data_dict['url'],
                        user_id=user_id
                    )
                    print(new_movie)
                    self.session.add(new_movie)
                    self.session.commit()
                    return new_movie  # Return the newly added movie
                else:
                    print("User not found")
                    return None
        except Exception as e:
            print(f"Error adding movie: {str(e)}")
            self.session.rollback()
            return None

    def get_user_movies(self, user_id):
        try:
            user_movies = self.session.query(Movie).filter_by(user_id=user_id).all()
            movie_dict = {movie.id: movie for movie in user_movies}
            return movie_dict
        except Exception as e:
            print(f"Error retrieving movies for user {user_id}: {str(e)}")
            return {}

    def update_movie(self, user_id, movie_id, title, director, year, rating):
        try:
            movie = self.session.query(Movie).filter_by(id=movie_id, user_id=user_id).first()
            if movie:
                movie.title = title
                movie.director = director
                movie.year = year
                movie.rating = rating
                self.session.commit()
                return movie
            else:
                return []
        except Exception as e:
            print(f"Error in update_movie: {str(e)}")
            self.session.rollback()
            return []

    def delete_movie(self, user_id, movie_id):
        try:
            movie = self.session.query(Movie).filter_by(id=movie_id, user_id=user_id).first()
            if movie:
                self.session.delete(movie)
                self.session.commit()
                return True
            else:
                print("Movie not found for the user.")
                return False
        except Exception as e:
            print(f"Error deleting movie: {str(e)}")
            self.session.rollback()
            return False

    def delete_user(self, user_id):
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                return True
            else:
                print("User not found.")
                return False
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            self.session.rollback()
            return False
