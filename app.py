from flask import Flask, jsonify

app = Flask(__name__)


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
    return jsonify({'result': 'task ,22'})


if __name__ == "__main__":
    app.run(debug=True)
