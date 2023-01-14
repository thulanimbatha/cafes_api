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
    return jsonify(cafes=[to_dict(cafe) for cafe in cafes]), 200
    
@app.route('/search', methods=['GET'])
def search_cafe():
    # get search parameter from search bar
    search_location = request.args.get('loc')
    matching_cafe = Cafe.query.filter_by(location=search_location).first()
    if matching_cafe:
        return jsonify(cafe=to_dict(matching_cafe)), 200
    else:
        return jsonify(error={'Not Found': 'Sorry, we do not have a cafe at that location.'}), 404

## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."}), 200

## HTTP PUT/PATCH - Update Record
@app.route('/update/<cafe_id>', methods=['PATCH'])
def update(cafe_id):
    matching_cafe = db.session.query(Cafe).get(cafe_id)
    if matching_cafe:
        new_price = request.args.get('new_price')
        matching_cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={'Success': 'SUccessfully updated the price'}), 200
    else:
        return jsonify(error={'Not Found': 'Sorry a cafe with that id was not found in the database'}), 404


## HTTP DELETE - Delete Record
@app.route("/remove/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
