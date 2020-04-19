import os, time, datetime

from flask_restful import Resource, reqparse
from flask import Response, request
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
        callback_url = lnurl.lnurl_string + "/await-invoice"

        try:
            lnurl.save_to_db()
        except:
            return {"message": "An error occured inserting into the database"}, 500

        return (
            {"lnurl": "lightning:" + lnurl.lnurl_bech32(), "callback": callback_url},
            201,
        )


class LnurlAwait(Resource):
    def get(self, uuid):
        # db_entry = LnurlModel.find_by_uuid(uuid)
        # if not db_entry:
        #     return {"status": "ERROR", "reason": "Lnurl not found."}, 404

        invoice = ""
        while not invoice:
            invoice = LnurlModel.find_by_uuid(uuid).invoice_bech32
            time.sleep(1)
        return {"invoice": invoice}, 200


class LnurlRequest(Resource):
    def get(self, uuid):
        db_entry = LnurlModel.find_by_uuid(uuid)
        if db_entry:
            response = LnurlModel.lnurl_withdraw_response(db_entry)
            return response.dict(), 200
        return {"status": "ERROR", "reason": "Lnurl not found"}, 404


class LnurlWithdraw(Resource):
    def get(self, uuid):
        k1 = request.args.get("k1")
        invoice = request.args.get("pr")

        db_entry = LnurlModel.find_by_uuid(uuid)
        if not db_entry:
            return {"status": "ERROR", "reason": "Lnurl not found."}, 404

        if k1 != db_entry.k1:
            return {"status": "ERROR", "reason": "K1 not found"}, 404

        db_entry.invoice_bech32 = invoice
        if db_entry.validate_invoice():
            try:
                db_entry.save_to_db()
            except:
                {"message": "An error occured inserting into the database"}, 500
            return {"status": "OK"}, 200
        return {"status": "ERROR", "reason": "Invalid lightning invoice"}, 400
