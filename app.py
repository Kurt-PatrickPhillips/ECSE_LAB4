from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://brqiamww:WF8eGgGIb-64m4Lja2eKGKTNJB_Jk7kp@ziggy.db.elephantsql.com:5432/brqiamww"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

UserProfile = {
    "success": True,
    "data": {
        "last_updated": "",
        "username": "Hannibal",
        "role": "Engineer",
        "color": "yellow"
    }
}

class Tank(db.Model):
    __tablename__ = "tanks"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.String(50), nullable=False)
    long = db.Column(db.String(50), nullable=False)
    percentage_full = db.Column(db.Integer, nullable=False)

class TankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tank 
        fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "ECSELAB4"


#GET / Profile


@app.route("/profile", methods=["GET", "POST", "Patch"])
def get_profile():
    if request.method == "GET":
        return jsonify(UserProfile)

        if request.method == "POST":
            UserProfile["data"]["username"] = (request.json["username"])
            UserProfile["data"]["role"] = (request.json["role"])
            UserProfile["data"]["color"] = (request.json["color"])
            UserProfile["data"]["last_updated"] = datetime.now()

            return jsonify(UserProfile)

            if request.method == "PATCH":

                tempDict = request.json
                tempDict["last_updated"] = datetime.now()
                attributes = tempDict.keys()

            for attribute in attributes:
                UserProfile["data"][attribute] = tempDict[attribute]

    return jsonify(UserProfile)

#/
@app.route("/data")
def get_tanks():
    tanks = Tank.query.all()
    tanks_json = TankSchema(many=True).dump(tanks)
    return jsonify(tanks_json)

@app.route("/data", methods=["POST"])
def add_Tanks():
        newTank = Tank(
            location = request.json["location"],
            lat = request.json["lat"],
            long = request.json["long"],
            percentage_full = request.json["percentage_full"]
        )

        db.session.add(newTank)
        db.session.commit()
        return TankSchema().dump(newTank)


@app.route("/data/<int:id>", methods=["PATCH"])
def update_tank(id):
    tanks = Tank.query.get(id)
    update = request.json
    if "location" in update:
        tanks.location = update["location"]
    if "lat" in update:
        tanks.lat = update["lat"]
    if "long" in update:
        tanks.long = update["long"]
    if "percentage_full" in update:
        tanks.percentage_full = update["percentage_full"]
    
    db.session.commit()
    return TankSchema().dump(tanks)


@app.route("/data/<int:id>", methods=["DELETE"])
def delete_tank(id):
    tanks = Tank.query.get(id)
    db.session.delete(tanks)
    db.session.commit()
    return{"success": True}
    


if __name__ == '__main__':
    app.run(debug=True)