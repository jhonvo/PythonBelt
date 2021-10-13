from flask import Flask, render_template, redirect, session, request
from cardealz_app import app
from cardealz_app.models.cars import Car
from cardealz_app.models import users

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/car/new', methods=['POST', 'GET'])
def car_new():
    if not 'userid' in session:
        return redirect ('/')
    user_id = session['userid']
    return render_template ("new.html", user_id = user_id)

@app.route('/car/save', methods=['POST'])
def car_save():
    print (request.form)
    if not Car.car_validation(request.form):
        return redirect('/car/new')
    new_car = Car.savecar(request.form)
    return redirect ('/dashboard')
    
@app.route('/car/<int:id>')
def car_show(id):
    if not 'userid' in session:
        return redirect ('/')
    carinfo = Car.get_car(id)
    # print (carinfo.model)
    return render_template ("show.html", car = carinfo)


@app.route('/purchase/<int:id>', methods=['GET'])
def car_purchase(id):
    if not 'userid' in session:
        return redirect ('/')
    carupdate = Car.purchase_car(id)
    return redirect ('/user')

@app.route('/user')
def user_info():
    if not 'userid' in session:
        return redirect ('/')
    carsowned = Car.get_owned()
    data = session['userid']
    user = users.User.getuser(data)
    return render_template ("user.html", cars = carsowned, user = user)

@app.route('/car/edit/<int:id>', methods=['POST', 'GET'] )
def edit_car(id):
    if not 'userid' in session:
        return redirect ('/')
    carinfo = Car.get_car(id)
    return render_template ("edit.html", car = carinfo)


@app.route('/car/update/<int:id>', methods=['POST'])
def car_saveupdate(id):
    print (request.form)
    if not Car.car_validation(request.form):
        redirect_url = f"/car/edit/{id}"
        return redirect(redirect_url)
    update_car = Car.updatecar(request.form)
    return redirect ('/dashboard')

@app.route('/car/remove/<int:id>')
def car_remove(id):
    if not 'userid' in session:
        return redirect ('/')
    remove = Car.removecar(id)
    return redirect ('/dashboard')




