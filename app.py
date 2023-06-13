from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from models import db, Users

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/flask-api'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

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
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    print(name)
    print(email)
    print(password)

    users = Users(name=name, email=email, password=password)
    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)


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


if __name__ == "__main__":
    app.run(debug=True)
