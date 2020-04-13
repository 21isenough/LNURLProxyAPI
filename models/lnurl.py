from database import db
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
        self.max_withdrawable = amount
        self.min_withdrawable = amount
        self.tag = "withdrawRequest"
        self.default_description = "LightningATM LNURL Withdraw"
        self.create_date = datetime.now()

    def lnurl_bech32(self):
        return lnurl.encode(self.lnurl_string)

    def json(self):
        return {
            "uuid": self.uuid,
            "amount": self.amount,
            "lnurl_string": self.lnurl_string,
            "lnurl": self.lnurl,
            "k1": self.k1,
            "max_withdrawable": self.max_withdrawable,
            "min_withdrawable": self.min_withdrawable,
            "tag": self.tag,
            "default_description": self.default_description,
            "create_date": self.create_date.isoformat(),
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
