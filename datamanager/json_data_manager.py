import json
import requests
from .data_manager_interface import DataManagerInterface
import imdb
import uuid


API_KEY = "e2e17332"


class JSONDataManager(DataManagerInterface):
    """JSONDataManager class represents a storage for the JSON file"""
    def __init__(self, filename):
        """
        Initializes a new instance of the JSON file.

        Arg:
            filename(file path): The location of the JSON file.
        """
        self.filename = filename
        self.country_dict = {}

    def get_all_users(self):
        """
        Gets all the users from the JSON file.

        Return:
            data(list): List of all the users from the JSON file
        """
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            return list(data.values())

    def get_user_movies(self, user_id):
        """
        Gets all the movies of the user from the JSON file.

        Arg:
            user_id(str): The unique key or user id of the user.

        Return:
            user(dict): A dictionary of the movies of the indicated user.
        """
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            user = data.get(user_id)
            return user

    def get_user(self, user_id):
        """
        Gets all the  information of the user from the JSON file.

        Arg:
            user_id(str): The unique key or user id of the user.

        Return:
            user(dict): A dictionary of the information of the user.
        """
        with open(self.filename, 'r') as file:
            data = json.load(file)
            users = data.get('users', [])
            for user in users:
                if user['user_id'] == user_id:
                    return user
        return None

    def get_user_by_username(self, username):
        """
        Gets all the  information of the user using its username from the JSON file.

        Arg:
            username(str): The username of the user as indicated in the JSON file.

        Return:
            user(dict): A dictionary of the information of the user.
        """
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            for user_id, user in data.items():
                if user.get("username") == username:
                    user["user_id"] = user_id
                    return user
        return None

    def authenticate_user(self, username, password):
        """
        Authenticate the user by its username and password information as stored in the JSON file.

        Arg:
            username(str): The username of the user as indicated in the JSON file.
            password((str): The password of the user as indicated in the JSON file.

        Return:
            user(dict): A dictionary of the information of the user.
        """
        user = self.get_user_by_username(username)
        if user and user.get('password') == password:
            return user
        return None

    def add_user(self, name, username, password):
        """
        Allows user to add another user.

        Arg:
            name(str): The name of the user which will be used in the JSON file
            username(str): The username of the user which will be used ito access the movies in the JSON file.
            password(str): The password of the user which will be used to access the movies in the JSON file.

        Return:
            user_id(dict): A dictionary of the information of the user."""
        try:
            with open(self.filename, 'r') as file_obj:
                data = json.load(file_obj)
                existing_users = data.values()
                for user in existing_users:
                    if user['username'] == username or user['name'] == name:
                        return None

                # Generate a unique ID for the new user
                user_id = str(uuid.uuid4())

                user = {
                    "name": name,
                    "username": username,
                    "password": password,
                    "movies": {}
                }
                data[user_id] = user

            with open(self.filename, 'w') as file_obj:
                json.dump(data, file_obj, indent=4)

            return user_id
        except Exception as e:
            print(f'Error: {e}')
            return None

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

    @staticmethod
    def genre_maker(genre):
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

    @staticmethod
    def fetch_movie_details(title):
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url)
        if response.status_code == 200:
            movie_data = response.json()
            return movie_data
        return None

    def add_movie(self, user_id, title):
        """
        Adds a movie to the movies' database.
        Loads the information from the JSON file, add the movie,
        and saves it.

        Args:
            user_id(str): The unique id of the user.
            title(str): Title of the movie to be added.

        Raises:
            Exception: If the user id is not found
            Exception: Covers all the other error that might occur and explains user the reason.
        """
        movie_data = self.fetch_movie_details(title)

        # API for omdb
        url_omd = f"http://www.omdbapi.com/?apikey={API_KEY}&t="

        # To locate the URL of the added movie
        ia = imdb.IMDb()
        add_movie = ia.search_movie(title)
        movie = add_movie[0]
        ia.update(movie)
        imdb_url = ia.get_imdbURL(movie)

        # To create the flag image of the added movie
        add_url = url_omd + title
        movie = requests.get(add_url)
        res = movie.json()
        country = res["Country"]
        if "," in country:
            country = country.split(",")[0]
        country_code = self.get_country_code()
        country_origin = country_code[country]

        # To create the genre image of the added movie
        genre_source = res["Genre"]
        first_genre = genre_source.split(",")[0]
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
        if movie_data:
            try:
                with open(self.filename, 'r') as file_obj:
                    data = json.load(file_obj)
                    users = data.get(str(user_id), {})
                    user = dict(users)
                    if user:
                        movies = user.get('movies', {})
                        movie_id = str(len(movies) + 1)
                        movie = {
                            'title': movie_data.get('Title'),
                            'director': movie_data.get('Director'),
                            'year': movie_data.get('Year'),
                            'rating': movie_data.get('imdbRating'),
                            'poster': movie_data.get('Poster'),
                            'genre': movie_genre,
                            'flag': f'https://flagsapi.com/{country_origin}/shiny/64.png',
                            'url': imdb_url
                        }

                        # Check if the movie already exists in the user's movies
                        existing_movies = movies.values()
                        if any(existing_movie['title'] == title for existing_movie in existing_movies):
                            return  # Movie already exists, no need to add

                        movies[movie_id] = movie
                        user['movies'] = movies
                        with open(self.filename, 'w') as new_file:
                            json.dump(data, new_file, indent=4)
                    else:
                        raise Exception(f"User {user_id} not found.")
            except Exception as e:
                print(f'Error: {e}')

    def update_movie(self, user_id, movie_id, title, director, year, rating):
        """
        Updates a movie from the movies' database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.

        Args:
            user_id(str): The unique id of the user.
            movie_id(str): The movie id of the user's movie.
            title(str): Movie title to update.
            director(str): Director to update.
            year(int): Year to update.
            rating(float): Rating to update.
        """
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            user = data.get(user_id)
            if user:
                movies = user.get('movies', {})
                movie = movies.get(movie_id)
                if movie:
                    movie['title'] = title
                    movie['director'] = director
                    movie['year'] = year
                    movie['rating'] = rating
        with open(self.filename, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)

    def delete_movie(self, user_id, movie_id):
        """
        Deletes a movie from the movies' database.
        Loads the information from the JSON file, deletes the movie,
        and saves it.

        Args:
            user_id(str): The unique id of the user.
            movie_id(str): The movie id of the user's movie.

        """
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            user = data.get(user_id)
            if user:
                movies = user.get('movies', {})
                if movie_id in movies:
                    del movies[movie_id]
        with open(self.filename, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)

    def delete_user(self, user_id):
        """
        Deletes the user from the database.
        Loads the information from the JSON file, deletes the movie,
        and saves it.

        Args:
            user_id(str): The unique id of the user.
        """
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            if str(user_id) not in data:
                raise Exception(f"User {user_id} not found.")
            del data[str(user_id)]
        with open(self.filename, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)
