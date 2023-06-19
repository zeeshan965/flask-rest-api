from flask import Blueprint

users = Blueprint('users', __name__)


@users.route('/users')
def list_users():
    return 'List of users'


@users.route('/users/<user_id>')
def get_user(user_id):
    return f'User with ID: {user_id}'
