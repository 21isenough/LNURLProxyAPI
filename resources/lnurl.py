import os, time, datetime

from flask_restful import Resource, reqparse
from models.lnurl import LnurlModel


class LnurlCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "amount",
        type=int,
        required=True,
        help="To request a lnurl, you must provide 'amount' (int)",
    )

    def post(self):
        data = self.parser.parse_args()

        lnurl = LnurlModel(**data)
        print(lnurl.json())

        try:
            lnurl.save_to_db()
        except:
            return {"message": "An error occured inserting the lnurl"}, 500

        return lnurl.json(), 201


class LnurlAwait(Resource):
    def get(self, uuid):
        print(uuid)
        request_time = time.time()
        while not (os.stat("data.txt").st_mtime > request_time):
            time.sleep(0.5)
        content = ""
        with open("data.txt") as data:
            content = data.read()
        return {"content": content}


class LnurlRequest(Resource):
    def get(self, uuid):
        print(uuid)
        return {"status": "OK"}, 200


class LnurlWithdraw(Resource):
    def get(self, uuid):
        k1 = request.args.get("k1")
        invoice = request.args.get("pr")
        print(k1, invoice, uuid)
        with open("data.txt", "w+") as file:
            file.write(invoice)
        return {"status": "OK"}, 200
