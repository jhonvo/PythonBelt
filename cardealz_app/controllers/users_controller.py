from flask import Flask, render_template, redirect, session, request
from cardealz_app import app
from cardealz_app.models.users import User
from cardealz_app.models import cars

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    if not 'userid' in session:
        return render_template('index.html')
    return redirect ('/dashboard')

@app.route('/register', methods=['POST'])
def register():
    if not User.register_validation(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'password' : pw_hash,
        'email' : request.form['email'],
        }
    newUser = User.register(data)
    session['userid'] = newUser
    return redirect ('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.login_validation(request.form):
        return redirect ('/')
    return redirect ('/dashboard')

@app.route('/dashboard')
def user():
    if not 'userid' in session:
        return redirect ('/')
    data = session['userid']
    user = User.getuser(data)
    carslist = cars.Car.getallcars()
    # print (carslist[0].model)
    return render_template('dashboard.html', cars = carslist, user = user)
    # print (user.first_name)
    # return "Hello"

@app.route('/logout', methods=['GET'])
def restart():
    session.clear()
    return redirect('/')