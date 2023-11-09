"""
===========================================================
                  Movie Web Application
        Flask Web Application with Database Storage
              By Frelin C. Ogario Johnson
===========================================================
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_cors import CORS
import secrets
from datamanager.sqlite_data_manager import SQLiteDataManager
from datamanager.sql_model import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Admin/PycharmProjects/ProjectPhase5/MoviWeb_App/storage/movies.sqlite'
db.init_app(app)
CORS(app)
data_manager = SQLiteDataManager('C:/Users/Admin/PycharmProjects/ProjectPhase5/MoviWeb_App/storage/movies.sqlite')


# Configure LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view endpoint

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


@app.route('/')
def home():
    return render_template('login.html', welcome_message="Welcome to MovieWeb App!")


@app.route('/users')
def list_users():
    """
    Route handler for listing users.

    Retrieves all users from the data manager.
    Renders the 'users.html' template with the users' data.

    Returns:
        Rendered template for displaying users.
        In case of an error, returns an error message string.
    """
    try:
        users = data_manager.get_all_users()
        users_dict = {str(i + 1): user for i, user in enumerate(users)}
        return render_template('users.html', users=users_dict)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            data_manager.add_user(name, username, password)
            return redirect(url_for('list_users'))
        return render_template('add_user.html')
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route handler for adding a new movie for a user.

    Args:
        user_id (str): The ID of the user to add the movie for.

    Returns:
        If the request method is POST, redirects to the 'user_movies' route for the same user.
        If the request method is GET, renders the 'add_movie.html' template with the user_id.
        In case of an error, returns an error message string.
    """
    try:
        if request.method == 'POST':
            title = request.form['title']
            data_manager.add_movie(user_id, title)
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('add_movie.html', user_id=user_id)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>')
def user_movies(user_id):
    """
    Route handler for displaying movies for a specific user.

    Args:
        user_id: ID of the user for whom the movies are being displayed.

    Returns:
        Rendered template for displaying the user's movies.
        If the user is not found, returns a string indicating the user was not found.
        In case of an error, returns an error message string.
    """
    try:
        user = data_manager.get_user_movies(user_id)
        if user_movies is None:
            return render_template('error.html', error_message='User not found')

        return render_template('sql_user_movies.html', user=user, user_id=user_id)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route handler for updating a movie for a user.

    Args:
        user_id (str): The ID of the user.
        movie_id (str): The ID of the movie to update.

    Returns:
        If the request method is POST, redirects to the 'user_movies' route for the same user.
        If the request method is GET, renders the 'update_movie.html' template.
        In case of an error, returns an error message string.
    """
    try:
        if request.method == 'POST':
            title = request.form['title']
            director = request.form['director']
            year = int(request.form['year'])
            rating = float(request.form['rating'])
            success = data_manager.update_movie(user_id, movie_id, title, director, year, rating)

            if success:
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return render_template('error.html', error_message='Movie update failed')

        user_movies = data_manager.get_user_movies(user_id)
        if user_movies is None:
            return render_template('error.html', error_message='User not found')

        movie = user_movies.get(int(movie_id))
        if movie is None:
            return render_template('error.html', error_message='Movie not found')

        return render_template('update_movie.html', user_movies=user_movies, movie=movie, user_id=user_id, movie_id=movie_id)

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    """
    Route handler for deleting a movie for a user.

    Args:
        user_id (str): The ID of the user.
        movie_id (str): The ID of the movie to delete.

    Returns:
        Redirects to the 'user_movies' route for the same user ID.
        In case of an error, returns an error message string.
    """
    try:
        data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/delete_user')
def delete_user(user_id):
    """
    Route handler for deleting a user.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        Redirects to the 'list_users' route.
        In case of an error, returns an error message string.
    """
    try:
        data_manager.delete_user(str(user_id))
        return redirect(url_for('list_users'))
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.errorhandler(404)
def page_not_found(e):
    """It handles the error if the page is not found."""
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """It handles the error if the method is not allowed."""
    return render_template('405.html'), 405


class UserLog(UserMixin):
    """ Define a UserLog model that implements the UserMixin from Flask-Login. """
    def __init__(self, user_id, username, password):
        """Initialize a UserLog object.

        Args:
            user_id (str): The ID of the user.
        """
        self.id = user_id
        self.username = username
        self.password = password

    @property
    def is_authenticated(self):
        return True  # You can customize this based on your authentication logic

    @property
    def is_active(self):
        return True  # You can customize this based on your user activation logic

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """
        Returns the unique identifier for the user.

        Returns:
            str: The user's unique identifier.
        """
        return str(self.id)

    @staticmethod
    def get(user_id):
        """
        Retrieve a user from the data manager or database based on the provided user_id.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            UserLog or None: The user object if found, or None if the user does not exist.
        """
        return data_manager.get_user(user_id)


@login_manager.user_loader
def load_user(user_id):
    """
    Callback function to load a user object from the user ID.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        UserLog or None: The user object if found, or None if the user does not exist.
    """
    return UserLog.get(user_id)


# Route for handling user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route handler for user login.

    Returns:
        GET: The rendered login template.
        POST: Redirect to the user_movies page if authentication is successful, otherwise the login template.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the data manager or database
        user = data_manager.authenticate_user(username, password)

        if user:
            # Use Flask-Login's login_user function to log in the user
            user_log = UserLog(user_id=user.id, username=user.username, password=user.password)
            login_user(user_log)

            # Redirect to the user_movies page
            return redirect(url_for('user_movies', user_id=user.id))

        # Authentication failed, show an error message
        flash('Invalid username or password', 'error')

    return render_template('login.html')


# Route for handling user logout
@app.route('/logout')
@login_required
def logout():
    """
    Route handler for user logout.

    Returns:
        Redirect to the home page.
    """
    # Use Flask-Login's logout_user function to log out the current user
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)