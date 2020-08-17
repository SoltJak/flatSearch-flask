from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), index=True)
    district = db.Column(db.String(64), index=True)
    roomsNo = db.Column(db.String(64))
    size = db.Column(db.String(64))
    price = db.Column(db.String(64))
    pricePerM2 = db.Column(db.String(64))
    link = db.Column(db.String(64))

    def __repr__(self):
        return 'Mieszkanie: {}m2, pokoi: {}, w cenie: {}PLN, Dzielnica: {}'.format(self.size, self.roomsNo, self.price, self.district)