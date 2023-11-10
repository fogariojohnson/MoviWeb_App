from .sql_model import db, User, Movie, Review
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .data_manager_interface import DataManagerInterface
import imdb
import requests


class SQLiteDataManager(DataManagerInterface):
    """SQLiteDataManager class represents a storage for the database file"""
    def __init__(self, db_file_name):
        """
        Initializes a new instance of the databse file.

        Arg:
            filename(file path): The location of the database file.
        """

        # Create an SQLAlchemy engine
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        # Create a session factory using the engine
        Session = sessionmaker(bind=self.engine)
        # Initialize a session
        self.session = Session()
        self.country_dict = {}

    def get_all_users(self):
        """
        Gets all the users from the database file.

        Return:
            users(list): List of all the users from the database file
        """
        try:
            users = self.session.query(User).all()
            return users
        except Exception as e:
            print(f"Error in get_all_users: {str(e)}")
            return []

    def add_user(self, name, username, password):
        """
        Allows user to add another user.

        Arg:
            name(str): The name of the user which will be used in the database file
            username(str): The username of the user which will be used ito access the movies in the database file.
            password(str): The password of the user which will be used to access the movies in the database file.
        """
        new_user = User(name=name, username=username, password=password)
        self.session.add(new_user)
        self.session.commit()

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
        """
        Fetches information about a movie using its title from the IMDb database.

        Args:
            title (str): The title of the movie to retrieve information for.

        Returns:
            new_movie(dict): A dictionary containing various details about the movie.
                        The dictionary includes the movie title, director(s), release year, rating,
                        poster URL, genre(s) with corresponding emoticons, the country's flag, and IMDb URL.
        """
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
        """
        Adds a movie to the movies' database.
        Loads the information from the database file, add the movie, and saves it.

        Args:
            user_id(str): The unique id of the user.
            title(str): Title of the movie to be added.

        Raises:
            Exception: Covers all the possible errors that might occur and explains user the reason.
        """
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
        """
         Gets all the movies of the user from the database file.

        Arg:
            user_id(str): The unique key or user id of the user.

        Return:
            movie_dict(dict): A dictionary of the movies of the indicated user.
        """
        try:
            user_movies = self.session.query(Movie).filter_by(user_id=user_id).all()
            movie_dict = {movie.id: movie for movie in user_movies}
            return movie_dict
        except Exception as e:
            print(f"Error retrieving movies for user {user_id}: {str(e)}")
            return {}

    def update_movie(self, user_id, movie_id, title, director, year, rating):
        """
        Updates a movie from the movies' database.
        Loads the information from the database file, updates the movie,
        and saves it. The function doesn't need to validate the input.

        Args:
            user_id(str): The unique id of the user.
            movie_id(str): The movie id of the user's movie.
            title(str): Movie title to update.
            director(str): Director to update.
            year(int): Year to update.
            rating(float): Rating to update.

        Return:
            movie or None: The updated Movie object if successful, else None.
        """
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
        """
        Deletes a movie from the movies' database.
        Loads the information from the database file, deletes the movie, and saves it.

        Args:
            user_id(str): The unique id of the user.
            movie_id(str): The movie id of the user's movie.

        """
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
        """
        Deletes the user from the database.
        Loads the information from the dataabase file, deletes the movie,
        and saves it.

        Args:
            user_id(str): The unique id of the user.
        """
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

    def get_user(self, user_id):
        """
        Gets all the  information of the user from the database.

        Arg:
            user_id(str): The unique key or user id of the user.

        Return:
            user(object): The object of the information of the user.
        """
        try:

            user = self.session.query(User).filter_by(id=user_id).first()

            if user:
                return user
            else:
                return None
        except Exception as e:
            print(f"Error retrieving user: {str(e)}")
            return None

    def get_user_by_id(self, user_id):
        """
        Retrieve a user from the database by their ID.

        Arguments:
            user_id (int): The unique identifier of the user to be retrieved.

        Returns:
            user(object): The user object with the specified ID exists.
        """
        session = self.session()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        return user

    def get_user_by_username(self, username):
        """
        Gets all the  information of the user using its username from the database.

        Argument:
            username(str): The username of the user as indicated in the JSON file.

        Return:
            user(object): An object of the information of the user.
        """
        session = self.session()
        user = session.query(User).filter(User.username == username).first()
        session.close()
        return user

    def authenticate_user(self, username, password):
        """
        Authenticate the user by its username and password information as stored in the database file.

        Arguments:
            username(str): The username of the user as indicated in the JSON file.
            password((str): The password of the user as indicated in the JSON file.

        Return:
            user(object): An object of the information of the user.
        """
        user = self.session.query(User).filter(User.username == username, User.password == password).first()
        return user

    def get_movie_reviews(self, user_id, movie_id):
        """
        Gets all reviews for a specific movie by a user.

        Args:
            user_id (str): The unique id of the user.
            movie_id (str): The movie id.

        Returns:
            list: List of reviews for the specified movie by the user.
        """
        try:
            reviews = self.session.query(Review).filter_by(user_id=user_id, movie_id=movie_id).all()
            return reviews
        except Exception as e:
            print(f"Error in get_movie_reviews: {str(e)}")
            return []

    def edit_review(self, user_id, movie_id, review_text, rating):
        """
        Edits an existing review for a movie by a user.

        Args:
            user_id (str): The unique id of the user.
            movie_id (str): The movie id.
            review_text (str): The updated review text.
            rating (float): The updated rating.

        Returns:
            bool: True if the review is successfully edited, False otherwise.
        """
        try:
            review = self.session.query(Review).filter_by(user_id=user_id, movie_id=movie_id).first()
            if review:
                review.review_text = review_text
                review.rating = rating
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error in edit_review: {str(e)}")
            self.session.rollback()
            return False

    def add_review(self, user_id, movie_id, review_text, rating):
        """
        Adds a new review for a movie by a user.

        Args:
            user_id (str): The unique id of the user.
            movie_id (str): The movie id.
            review_text (str): The review text.
            rating (float): The rating.

        Returns:
            bool: True if the review is successfully added, False otherwise.
        """
        try:
            new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, rating=rating)
            self.session.add(new_review)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error in add_review: {str(e)}")
            self.session.rollback()
            return False

    def delete_review(self, user_id, movie_id):
        """
        Deletes a review for a movie by a user.

        Args:
            user_id (str): The unique id of the user.
            movie_id (str): The movie id.

        Returns:
            bool: True if the review is successfully deleted, False otherwise.
        """
        try:
            review = self.session.query(Review).filter_by(user_id=user_id, movie_id=movie_id).first()
            if review:
                self.session.delete(review)
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error in delete_review: {str(e)}")
            self.session.rollback()
            return False
