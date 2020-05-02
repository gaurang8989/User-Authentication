from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from bson.json_util import dumps, ObjectId
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secreatkey"

app.config['MONGO_URI'] = "mongodb://gaurang:123123123@cluster0-shard-00-00-pijjr.mongodb.net:27017,cluster0-shard-00-01-pijjr.mongodb.net:27017,cluster0-shard-00-02-pijjr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def goto_index():
    return render_template('login.html', a="hello from server")


@app.route('/login', methods=['POST'])
def my_login():
    a = request.form['username']
    b = request.form['pwd']

    if a and b and request.method == 'POST':
        user = mongo.db.login.find({'name': a}, {'_id': 0, 'name': 0})
        if(user):
            temp = ""
            for i in user:
                temp = i['password']
            if check_password_hash(temp, b):
                return render_template("show.html", a=a)
    return render_template("error.html")


@app.route('/signup.html', methods=['POST', 'GET'])
def render_signup():
    return render_template("signup.html")


@app.route('/signup', methods=['POST', 'GET'])
def add_user():
    a = request.form['username']
    b = request.form['pwd']
    c = request.form['pwdc']

    if a and b and c and request.method == "POST":
        _hashed = generate_password_hash(b)

        if check_password_hash(_hashed, c):
            id = mongo.db.login.insert({"name": a, "password": _hashed})
            return render_template("show.html", a=a)

    return render_template("error.html")


if __name__ == '__main__':
    app.run()
