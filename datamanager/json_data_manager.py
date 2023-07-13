import os
import json
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            users = data.get('users', {})
            return list(users.values())

    def get_user_movies(self, user_id):
        with open(self.filename, 'r') as file_obj:
            data = json.load(file_obj)
            users = data.get('users', {})
            user = users.get(str(user_id))
            if user:
                return user.get('movies', {})
            return {}


    def      