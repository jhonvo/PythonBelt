from flask.globals import session
from cardealz_app.config.mysqlconnection import connectToMySQL
from cardealz_app import app
from cardealz_app.models import users
from flask import flash

import re
NUMBER_REGEX = re.compile(r'^[0-9]+$')

class Car:
    def __init__(self,data):
        self.id = data['id']
        self.model = data['model']
        self.price = data['price']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
        self.seller = data['first_name']

    @classmethod
    def getallcars(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON seller_id = users.id;"
        results = connectToMySQL('cardealz').query_db(query)
        # print (results)
        carlist = []
        for line in results:
            carlist.append(Car(line))
        return carlist

    @staticmethod
    def car_validation(data):
        is_valid = True
        if  not NUMBER_REGEX.match(data['price']) or int(data['price']) <= 0:
            flash("Please provide a valid price.")
            is_valid=False
        if len(data['model']) < 3:
            flash("Please provide a valid Model.")
            is_valid=False
        if len(data['make']) < 3:
            flash("Please provide valid Make.")
            is_valid=False
        if not NUMBER_REGEX.match(data['year']) or  int(data['year']) <= 0:
            flash("Please provide a valid year.")
            is_valid=False
        if len(data['description']) > 250 or len(data['description']) < 3:
            flash("Description should be more than 3 characters and less than 250 characters.")
            is_valid=False
        return is_valid

    @classmethod
    def savecar(cls,data):
        query = "INSERT INTO cars (price,model,make,year,description,seller_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(seller_id)s);"
        results = connectToMySQL('cardealz').query_db(query,data)
        return results

    @classmethod
    def get_car(cls,id):
        query = "SELECT * FROM cars LEFT JOIN users ON seller_id = users.id WHERE cars.id = %(id)s;"
        data = {
            'id' : id
        }
        results = connectToMySQL('cardealz').query_db(query,data)
        car = []
        for line in results:
            car.append(Car(line))
        print (car[0].id)
        return car[0]

    @classmethod
    def purchase_car(cls,id):
        query = "UPDATE cars SET buyer_id = %(buyer_id)s WHERE cars.id = %(id)s;"
        buyerid = session['userid']
        data = {
            'id' : id,
            'buyer_id' : buyerid
        }
        results = connectToMySQL('cardealz').query_db(query,data)
        return results

    @classmethod
    def get_owned(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON buyer_id = users.id WHERE buyer_id = %(id)s;"
        id = session['userid']
        data = {
            'id' : id
        }
        results = connectToMySQL('cardealz').query_db(query,data)
        return results

    @classmethod
    def updatecar(cls,data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL('cardealz').query_db(query,data)
        return results

    @classmethod
    def removecar(cls,id):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        data = {
                'id' : id
            }
        results = connectToMySQL('cardealz').query_db(query,data)
        return results


