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
from datamanager.sql_model import db, Review
from sqlalchemy.exc import IntegrityError
from api import api_bp


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
    """The Welcome message of the app."""
    return render_template('login.html', welcome_message="Welcome to MovieWeb App!")


@app.route('/users')
def list_users():
    """
    Route handler for listing users.

    Retrieves all users from the data manager.
    Renders the 'users.html' template with the users' data.

    Returns:
        Rendered template for displaying users.
        In case of an error, returns an error message template.
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
    """
    Route handler for adding a new user.

    Returns:
        If the request method is POST, redirects to the 'list_users' route.
        If the request method is GET, renders the 'add_user.html' template.
        In case of an error, returns an error message template.
    """
    try:
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            data_manager.add_user(name, username, password)
            return redirect(url_for('list_users'))
        return render_template('add_user.html')

    except IntegrityError as integrity_error:
        error_message = f"Error adding user: {str(integrity_error)}. The name or username already exists."
        return render_template('error.html', error_message=error_message)

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
        In case of an error, returns an error message template.
    """
    try:
        if request.method == 'POST':
            title = request.form['title']
            data_manager.add_movie(user_id, title)
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('add_movie.html', user_id=user_id)

    except TypeError as type_error:
        error_message = f"Type error occurred: {str(type_error)}"
        return render_template('error.html', error_message=error_message)

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
        In case of an error, returns an error message template.
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
        In case of an error, returns an error message template.
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

    except IntegrityError as integrity_error:
        # Handle the specific IntegrityError related to the database constraint
        error_message = f"Error updating movie: {str(integrity_error)}. Allowed rating is from 1-10."
        return render_template('error.html', error_message=error_message)

    except Exception as e:
        # Handle other general exceptions
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
        In case of an error, returns an error message template.
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
        In case of an error, returns an error message template.
    """
    try:
        data_manager.delete_user(str(user_id))
        return redirect(url_for('list_users'))
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/reviews/<movie_id>')
def movie_review(user_id, movie_id):
    """
    Route handler for movie review.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        Redirects to the 'movie review' route.
        In case of an error, returns an error message template.
    """
    try:
        reviews = data_manager.get_movie_reviews(user_id, movie_id)
        return render_template('movie_review.html', reviews=reviews, user_id=user_id, movie_id=movie_id)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/edit_review/<movie_id>', methods=['GET', 'POST'])
def edit_review(user_id, movie_id):
    """
    Route handler for movie review that needs to be edited.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        Redirects to the 'user movies' route.
        In case of an error, returns an error message template.
    """
    try:
        existing_review = data_manager.session.query(Review).filter_by(user_id=user_id, movie_id=movie_id).first()

        if request.method == 'POST':
            updated_review_text = request.form.get('review_text')
            updated_rating = float(request.form.get('rating'))
            success = data_manager.edit_review(user_id, movie_id, updated_review_text, updated_rating)

            if success:
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                error_message = 'Failed to update review'
                return render_template('error.html', error_message=error_message)

        # Pass the existing_review variable to the template
        return render_template('edit_review.html', user_id=user_id, movie_id=movie_id, existing_review=existing_review)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/add_review/<movie_id>', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    """
    Route handler for to add a review for a movie.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        Redirects to the 'movie review' route.
        In case of an error, returns an error message template.
    """
    try:
        if request.method == 'POST':
            review_text = request.form['review_text']
            rating = request.form['rating']
            data_manager.add_review(user_id, movie_id, review_text, rating)
            return redirect(url_for('movie_review', user_id=user_id, movie_id=movie_id))
        return render_template('add_review.html', user_id=user_id, movie_id=movie_id)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/delete_review/<movie_id>', methods=['GET', 'POST'])
def delete_review(user_id, movie_id):
    """
    Route handler to delete a review for a movie.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        Redirects to the 'movie review' route.
        In case of an error, returns an error message template.
    """
    try:
        data_manager.delete_review(user_id, movie_id)
        return redirect(url_for('movie_review', user_id=user_id, movie_id=movie_id))
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


app.register_blueprint(api_bp, url_prefix='/api')


class User(UserMixin):
    """ Define a User model that implements the UserMixin from Flask-Login. """
    def __init__(self, user_id):
        """Initialize a User object.

        Args:
            user_id (str): The ID of the user.
        """
        self.id = user_id

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
            User or None: The user object if found, or None if the user does not exist."""
        return data_manager.get_user(user_id)


@login_manager.user_loader
def load_user(user_id):
    """
    Callback function to load a user object from the user ID.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        User or None: The user object if found, or None if the user does not exist."""
    return User.get(user_id)


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
            user_id = user.id
            login_user(User(user_id))

            # Redirect to the user_movies page
            return redirect(url_for('user_movies', user_id=user.id))

        # Authentication failed, show an error message
        flash('Invalid username or password', 'error')

    # Render the login template
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
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
