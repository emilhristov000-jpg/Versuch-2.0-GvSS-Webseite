from . import crypting
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from datetime import datetime, timezone
import uuid

fake = Faker("de_DE")
db = SQLAlchemy()

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

    klasse = db.Column(
        db.String(20),
        nullable=True
    )

class Fach(db.Model):
    __tablename__ = "Fach"

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
        db.ForeignKey("Fach.id"),
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

def erstellung(mail, password, name, nachname, klasse=None):
    user = User(
        mail=mail.strip().lower(),
        password=crypting.pasoschlsl(password),
        name=name,
        nachname=nachname,
        klasse=klasse,
        last_log=datetime.now(timezone.utc),
        online=True,
        trys=0,
    )

    db.session.add(user)
    db.session.commit()
    return user


def suche(wow):
    email_clean = str(wow or "").strip().lower()
    return User.query.filter_by(mail=email_clean).first()


def idsuche(wow):
    return User.query.filter_by(name=wow).scalar()
