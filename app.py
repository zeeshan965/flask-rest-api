from flask import Flask, jsonify
from models import db, Users

app = Flask(__name__)

app.config['SECRET_KEY'] = "my-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/flask-api"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    print('Hello, World!')
    return "<p>Hello, World!</p>"


@app.route("/users", methods=['GET'])
def list_users():
    return jsonify({'result': 'show all data'})


@app.route("/tasks", methods=['GET'])
def tasks():
    return jsonify({'result': 'show all tasks'})


@app.route("/tasks/show", methods=['GET'])
def show_task():
    return jsonify({'result': 'task 1'})


if __name__ == "__main__":
    app.run(debug=True)
