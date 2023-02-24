from datetime import datetime
from imkertagebuch import db, login_manager
from flask_login import UserMixin


# Test Ende 
# Für Sesseions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)            # erzeugt Relationship zu anderem Model # durch festlegen backref lässt sich User des Post durch post.author ermitteln 
    stockEintraege = db.relationship('StockEintrag', backref='autor')            # erzeugt Relationship zu anderem Model 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)       # TODO Zeitzone anpassen???
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)           # Fremdschlüssel für Relationship festlegen

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class StockEintrag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)       # TODO Zeitzone anpassen???
    # Allgemeiner Befund
    wabenbelegt = db.Column(db.Integer, default=0)
    brutw = db.Column(db.Boolean)
    brutei = db.Column(db.Boolean)
    brut_offen = db.Column(db.Boolean)
    brut_verdeckt = db.Column(db.Boolean)
    futter_kg = db.Column(db.Integer)
    wabensitz = db.Column(db.String(20))
    brutposition = db.Column(db.String(20))
    sanftmut = db.Column(db.Integer, default=5)
    # gegeben / entnommen 
    veraend_waben = db.Column(db.Integer)
    veraend_mittelwand = db.Column(db.Integer)
    veraend_brut = db.Column(db.Integer)
    veraend_drohnenrahmen = db.Column(db.Integer)
    veraend_bienen = db.Column(db.Integer)
    veraend_honig_kg = db.Column(db.Integer)
    einfutter_text = db.Column(db.String(150))
    kommentar = db.Column(db.String(150))
    # Relationships 
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stockkarten_id = db.Column(db.Integer, db.ForeignKey('stock_karte.id'), nullable=False)
    beute_id = db.Column(db.Integer, db.ForeignKey('beute.id'))
    # title = db.Column(db.String(100))

    def __repr__(self):
        return f"StockEintrag('{self.wabenbelegt}', '{self.date_posted}', '{self.brutw}, '{self.brutei}, '{self.brut_offen}, '{self.brut_verdeckt}', '{self.brutposition}', '{self.futter_kg}')"    # , , '{self.user_}', '{self.date_posted}'

class StockKarte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beute_id = db.Column(db.Integer, db.ForeignKey('beute.id'))                         # TODO add nullable false 
    standmass = db.Column(db.String(50))
    eintrag_id = db.relationship('StockEintrag', backref='karte')

    def __repr__(self):
        return f"StockKarte('{self.standmass}', '{self.id}')"

class Beute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    name = db.Column(db.String(50))
    standort = db.Column(db.String(50))
    lat = db.Column(db.String(50))
    long = db.Column(db.String(50))
    nummer = db.Column(db.String(5))
    stockkarte_id = db.relationship('StockKarte', backref='beute')

    def __repr__(self):
        return f"Beute('{self.name}', '{self.nummer}', '{self.standort}', '{self.stockkarte_id}')"
"""
    veraend_waben = db.Column(db.Integer)
    veraend_mittelwand = db.Column(db.Integer)
    veraend_brut = db.Column(db.Integer)
    veraend_drohnenrahmen = db.Column(db.Integer)
    veraend_bienen = db.Column(db.Integer)
    veraend_honig_kg = db.Column(db.Integer)
    einfutter_text = db.Column(db.String(150))
    kommentar = db.Column(db.String(150))
    wetter = db.Column(db.String(150))
    autor = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150)) 
"""

## Test 
db.create_all()
print('done')

