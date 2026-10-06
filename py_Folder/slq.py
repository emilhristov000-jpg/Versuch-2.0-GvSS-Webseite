from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid
from . import crypting

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

    def __init__(self, mail: str, password: str, name: str, nachname: str, klasse: str | None=None, last_log: datetime | None=None, online: bool=False, trys: int=0, rolle: str | None="Schüler"):
        self.mail = mail
        self.password = password
        self.name = name
        self.nachname = nachname
        self.klasse = klasse
        self.last_log = last_log or datetime.now(timezone.utc)
        self.online = online
        self.trys = trys
        self.rolle = rolle

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

    def __init__(self, fachname):
        self.fachname = fachname

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

    def __init__(self, user_id, fach_id):
        self.user_id = user_id
        self.fach_id = fach_id

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

    def __init__(self, beuzugsdaten, date, standpunkt):
        self.beuzugsdaten = beuzugsdaten
        self.date = date
        self.standpunkt = standpunkt

class Lehrer(db.Model):
    __tablename__ = "lehrer"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = db.Column(
        db.String(20),
        nullable=False
    )

    nachname = db.Column(
        db.String(30),
        nullable=False
    )

    Unterichtid = db.Column(
        db.String(36),
        db.ForeignKey("Fach.id"),
        nullable=False
    )

    def __init__(self, name, nachname, Unterichtid):
        self.name = name
        self.nachname = nachname
        self.Unterichtid = Unterichtid 


def erstellung(mail, password, name, nachname, klasse):
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

def lehrer_erstellung(name, nachname, unterichtid):
    user = Lehrer(
        name=name,
        nachname=nachname,
        Unterichtid=unterichtid
    )

    db.session.add(user)
    db.session.commit()
    return user

def fach_erstellung(fachname):
    user = Fach(
        fachname=fachname
    )

    db.session.add(user)
    db.session.commit()
    return user

def userfach_erstellung(user_id, fach_id):
    user = UserFach(
        user_id=user_id,
        fach_id=fach_id
    )

    db.session.add(user)
    db.session.commit()
    return user

def termin_erstellung(beuzugsdaten, date, standpunkt):
    user = Termin(
        beuzugsdaten=beuzugsdaten,
        date=date,
        standpunkt=standpunkt
    )

    db.session.add(user)
    db.session.commit()
    return user


def suche(wow):
    email_clean = str(wow or "").strip().lower()
    return User.query.filter_by(mail=email_clean).first()


def idsuche(wow):
    return User.query.filter_by(name=wow).scalar()
