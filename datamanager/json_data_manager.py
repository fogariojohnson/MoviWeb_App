import json
import requests
from .data_manager_interface import DataManagerInterface


API_KEY = "e2e17332"


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            return list(data.values())

    def get_user_movies(self, user_id):
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            user = data.get(user_id)
            return user

    def add_user(self, name):
        try:
            with open(self.filename, 'r') as file_obj:
                data = json.load(file_obj)
                existing_users = data.values()
                for user in existing_users:
                    if user['name'] == name:
                        return None

                user_id = str(len(data) + 1)
                user = {
                    "name": name,
                    "movies": {}
                }
                data[user_id] = user

            with open(self.filename, 'w') as file_obj:
                json.dump(data, file_obj, indent=4)

            return user_id
        except Exception as e:
            print(f'Error: {e}')
            return None

    @staticmethod
    def fetch_movie_details(title):
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url)
        if response.status_code == 200:
            movie_data = response.json()
            return movie_data
        return None

    def add_movie(self, user_id, title):
        movie_data = self.fetch_movie_details(title)
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
                            'rating': movie_data.get('imdbRating')
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
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            if str(user_id) not in data:
                raise Exception(f"User {user_id} not found.")
            del data[str(user_id)]
        with open(self.filename, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)



