from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from userSchema import FormSchema
from flask_cors import CORS, cross_origin
from models import db, Users
from markupsafe import escape
from flask import url_for
import pprint
from dotenv import load_dotenv
import os
from users.routes import users

load_dotenv()
app = Flask(__name__)

# Configuration options
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO')

app.register_blueprint(users)

CORS(app, supports_credentials=True)

db.init_app(app)

with app.app_context():
    db.create_all()

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/users', methods=['POST'])
def store():
    try:
        form_data = FormSchema().load(request.json)
        return jsonify({'message': 'Form data is valid'})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400


# name = request.json['name']
# email = request.json['email']
# password = request.json['password']
# print(name)
# print(email)
# print(password)
#
# users = Users(name=name, email=email, password=password)
# db.session.add(users)
# db.session.commit()
# return user_schema.jsonify(users)


@app.route('/users/<id>', methods=['GET'])
def show(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)


@app.route('/users/<id>', methods=['PUT'])
def update(id):
    user = Users.query.get(id)
    name = request.json['name']
    email = request.json['email']

    user.name = name
    user.email = email

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/users', methods=['GET'])
def index():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)


@app.route('/users/<id>', methods=['DELETE'])
def delete(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/test/<name>")
def hello(name):
    return f"Hello, {name}!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request)
    pprint.pprint(request.headers)
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def show_the_login_form():
    return 'login form'


def do_the_login():
    return 'login implementation'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == "__main__":
    app.run(debug=True)
