from flask import Blueprint, jsonify, request
from datamanager.sqlite_data_manager import SQLiteDataManager

api_bp = Blueprint('api', __name__)


data_manager = SQLiteDataManager('C:/Users/Admin/PycharmProjects/ProjectPhase5/MoviWeb_App/storage/movies.sqlite')


@api_bp.route('/users', methods=['GET'])
def list_all_users():
    users = data_manager.get_all_users()
    users_data = [{'id': user.id, 'name': user.name, 'username': user.username} for user in users]
    return jsonify(users_data)


@api_bp.route('/users/<int:user_id>/movies', methods=['GET'])
def list_user_favorite_movies(user_id):
    user = data_manager.get_user_movies(user_id)
    movie_dict = {}
    if not user:
        return jsonify({'message': 'User not found'}), 404
    for movie_id, movie in user.items():
        title = movie.title,
        year = movie.year
        rating = movie.rating
        reviews: movie.user_reviews
        movie_info = {
            'User ID': user_id,
            'title': title,
            'year': year,
            'rating': rating,
        }

        # Add the movie_info dictionary to the movie_dict using movie_id as the key
        movie_dict[movie_id] = movie_info

    user_data = {
        'id': user_id,
        'favorite_movies': movie_dict
    }
    return jsonify(user_data)


@api_bp.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_favorite_movie(user_id):
    if request.method == 'POST':
        title = request.form.get('title')
    movie = data_manager.add_movie(user_id, title)
    if movie:
        return jsonify({'message': 'Movie added successfully', 'movie_id': movie.id})
    else:
        return jsonify({'message': 'Error adding movie'}), 500
