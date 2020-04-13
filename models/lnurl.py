from database import db
from bech32 import bech32_decode
import lnurl
import config

from datetime import datetime
from random import choice
from uuid import uuid4


class LnurlModel(db.Model):

    __tablename__ = "lnurls"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    amount = db.Column(db.Integer)

    lnurl_string = db.Column(db.String(255))
    k1 = db.Column(db.String(64))
    max_withdrawable = db.Column(db.Integer)
    min_withdrawable = db.Column(db.Integer)
    tag = db.Column(db.String(255))
    default_description = db.Column(db.String(255))

    invoice_bech32 = db.Column(db.String(500))
    create_date = db.Column(db.DateTime)

    def __init__(self, amount):
        hex_characters = "0123456789abcdef"

        self.uuid = str(uuid4())
        self.amount = amount
        self.lnurl_string = (
            config.protocol + config.domain + config.path_prefix + self.uuid
        )
        self.k1 = "".join(choice(hex_characters) for _ in range(64))
        self.max_withdrawable = amount * 1000
        self.min_withdrawable = amount * 1000
        self.tag = "withdrawRequest"
        self.default_description = "LightningATM LNURL Withdraw"
        self.create_date = datetime.now()

    def lnurl_bech32(self):
        return lnurl.encode(self.lnurl_string)

    def lnurl_withdraw_response(self):
        response = lnurl.LnurlWithdrawResponse(
            callback=self.lnurl_string + "/withdraw",
            k1=self.k1,
            min_withdrawable=self.max_withdrawable,
            max_withdrawable=self.min_withdrawable,
            default_description=self.default_description,
        )
        return response

    def validate_invoice(self):
        hrp, data = bech32_decode(self.invoice_bech32)
        return hrp and data

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
