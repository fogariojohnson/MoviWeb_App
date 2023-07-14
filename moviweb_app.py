from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
CORS(app)
data_manager = JSONDataManager("storage/user.json")


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        return "An error occurred: " + str(e)


@app.route('/users/<user_id>')
def user_movies(user_id):
    try:
        user = data_manager.get_user_movies(user_id)
        if user is None:
            return "User not found"
        return render_template('user_movies.html', user=user)
    except Exception as e:
        return "An error occurred: " + str(e)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            name = request.form['name']
            user_id = data_manager.add_user(name)
            return redirect(f'/users/{user_id}')
        return render_template('add_user.html')
    except Exception as e:
        return "An error occurred: " + str(e)


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    try:
        if request.method == 'POST':
            title = request.form['title']
            data_manager.add_movie(user_id, title)
            return redirect(f'/users/{user_id}')
        return render_template('add_movie.html', user_id=user_id)
    except Exception as e:
        return "An error occurred: " + str(e)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    try:
        if request.method == 'POST':
            title = request.form['title']
            director = request.form['director']
            year = request.form['year']
            rating = request.form['rating']
            data_manager.update_movie(user_id, movie_id, title, director, year, rating)
            return redirect(f'/users/{user_id}')
        user = data_manager.get_user_movies(user_id)
        if user is None:
            return "User not found"
        movie = user['movies'].get(movie_id)
        if movie is None:
            return "Movie not found"
        return render_template('update_movie.html', user=user, movie=movie)
    except Exception as e:
        return "An error occurred: " + str(e)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(user_id, movie_id)
        return redirect(f'/users/{user_id}')
    except Exception as e:
        return "An error occurred: " + str(e)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
