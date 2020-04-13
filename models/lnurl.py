from database import db


class LnurlModel(db.Model):

    __tablename__ = "lnurls"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    amount = db.Column(db.Integer)
    # url_await_invoice = db.Column(db.String(255))

    # lnurl_string = db.Column(db.String(255))
    lnurl = db.Column(db.String(500))

    # url_withdraw = db.Column(db.String(255))
    k1 = db.Column(db.String(64))
    max_withdrawable = db.Column(db.Integer)
    min_withdrawable = db.Column(db.Integer)
    tag = db.Column(db.String(255))
    default_description = db.Column(db.String(255))

    invoice_bech32 = db.Column(db.String(500))
    create_date = db.Column(db.DateTime)

    def __init__(self, uuid, amount, lnurl):
        self.uuid = uuid
        self.amount = amount
        self.lnurl = lnurl
