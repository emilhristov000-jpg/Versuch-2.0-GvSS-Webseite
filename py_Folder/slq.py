from . import crypting
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
import uuid
from faker import Faker
from datetime import datetime,timezone

fake = Faker("de_DE")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///Schüler_Helfen_Schüler.db"
)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    last_log = db.Column(
       db.DateTime,
       nullable=False,
       default=lambda: datetime.now(timezone.utc)
    )

    online = db.Column(
       db.Boolean,
       nullable=False,
       default=False
    )

    trys =  db.Column(
       db.Integer,
       default=0
    )

    rolle = db.Column(
       db.String(12),
       nullable=False,
       default="Schüler"
    )

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    mail = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    name = db.Column(
        db.String(20),
        nullable=False
    )

    nachname = db.Column(
        db.String(30),
        nullable=False
    )

class Fach(db.Model):
    __tablename__ = "faecher"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    fachname = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

class UserFach(db.Model):
    __tablename__ = "user_faecher"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    fach_id = db.Column(
        db.String(36),
        db.ForeignKey("faecher.id"),
        nullable=False
    )

class Termin(db.Model):
    __tablename__ = "termine"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    beuzugsdaten = db.Column(
        db.String(36),
        db.ForeignKey("user_faecher.id"),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )
    standpunkt = db.Column(
        db.String(15),
        nullable=False
    )

with app.app_context():
  db.create_all()

def erstellung(mail, password, name, nachname):
  _mail = mail.strip().lower()
  with app.app_context():
    user = User(mail=_mail,
                password=crypting.pasoschlsl(password),
                name=name,
                nachname=nachname,
                last_log=datetime.now(timezone.utc),
                online=True,
                trys=0)

    db.session.add(user)
    db.session.commit()

#abcdefghijklnmop = ("emo", "emo", "emo", "emo")
#qrstovxyz = ()

#for i in abcdefghijklnmop:
#    qrstovxyz += (i,)
def fakeinerung(wow0):
    kabvddogn = 0
    while kabvddogn <= wow0:
        first_name = fake.first_name()
        last_name = fake.last_name()
        wow = erstellung(
            (f"{first_name}.{last_name}@gvss.de"), 
            fake.password(),
            first_name,
            last_name,
            )
        print(wow)
        kabvddogn+=1

def suche(wow):
   with app.app_context():
    email_clean = str(wow).strip().lower()
    return User.query.filter_by(mail=email_clean).first()

def idsuche(wow):
   User.query.filter_by(name=wow).scalar()