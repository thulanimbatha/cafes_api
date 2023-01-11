from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

app.app_context().push()
db.create_all()

# converting to a dictionary - for each table column entry
def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route('/random', methods=['GET'])
def random_cafe():
    # read database
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)

    return jsonify(cafe={
                    #"id": random_cafe.id,
                    "name": random_cafe.name,
                    "map_url": random_cafe.map_url,
                    "img_url": random_cafe.img_url,
                    "location": random_cafe.location,

                    # sub-category 
                    "amenities" : {
                        "seats": random_cafe.seats,
                        "has_toilet": random_cafe.has_toilet,
                        "has_wifi": random_cafe.has_wifi,
                        "has_sockets": random_cafe.has_sockets,
                        "can_take_calls": random_cafe.can_take_calls,
                        "coffee_price": random_cafe.coffee_price 
                        }
                    })

@app.route('/all', methods=['GET'])
def all_cafes():
    cafes = db.session.query(Cafe).all()
    
    # converts every cafe attribute into a dic entry then adds to list
    return jsonify(cafes=[to_dict(cafe) for cafe in cafes])
    

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
