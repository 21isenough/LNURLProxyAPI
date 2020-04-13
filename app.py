import os, time, datetime

from flask import Flask, request
from flask_restful import Api
from database import db

import resources.lnurl

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Thisisfornowmysecretkey"

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/v1/lnurl", methods=["POST"])
def home():
    request_data = request.get_json()
    print(request_data)
    return {"lnurl": "lnbcsomelnurl...", "callback": "https://somecallbackurl"}, 201


@app.route("/v1/lnurl/<string:uuid>/await-invoice")
def home1(uuid):
    print(uuid)
    request_time = time.time()
    while not (os.stat("data.txt").st_mtime > request_time):
        time.sleep(0.5)
    content = ""
    with open("data.txt") as data:
        content = data.read()
    return {"content": content}


@app.route("/v1/lnurl/<string:uuid>")
def home3(uuid):
    print(uuid)
    return {"status": "OK"}, 200


@app.route("/v1/lnurl/<string:uuid>/withdraw")
def home4(uuid):
    k1 = request.args.get("k1")
    invoice = request.args.get("pr")
    print(k1, invoice, uuid)
    with open("data.txt", "w+") as file:
        file.write(invoice)
    return {"status": "OK"}, 200


if __name__ == "__main__":
    app.run(debug=True)
