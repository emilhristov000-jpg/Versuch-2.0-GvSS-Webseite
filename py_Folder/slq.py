from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid
<<<<<<< HEAD
from . import crypting1
from sqlalchemy import ForeignKey
=======
from . import crypting
>>>>>>> f11c925 (Versuch Server Push)

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

    KlassenID = db.Column(
        db.String(20),
        ForeignKey("Klassen.id"),
        nullable=True
    )

    def __init__(self, mail: str, password: str, name: str, nachname: str, KlassenID: str | None=None, last_log: datetime | None=None, online: bool=False, trys: int=0, rolle: str | None="Schüler"):
        self.mail = mail
        self.password = password
        self.name = name
        self.nachname = nachname
        self.KlassenID = KlassenID
        self.last_log = last_log or datetime.now(timezone.utc)
        self.online = online
        self.trys = trys
        self.rolle = rolle

class Klassen(db.Model):
    __tablename__ = "Klassen"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    Klasse = db.Column(
        db.String(20),
        nullable=False
    )

    fachname = db.Column(
        db.String(25),
        nullable=False
    )

    def __init__(self, Klasse, fachname):
        self.Klasse = Klasse
        self.fachname = fachname

class HelferSchuler(db.Model):
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

<<<<<<< HEAD
    def __init__(self, beuzugsdaten, date, standpunkt):
        self.beuzugsdaten = beuzugsdaten
        self.date = date
        self.standpunkt = standpunkt

class Personal(db.Model):
    __tablename__ = "personal"
=======
class Lehrer(db.Model):
    __tablename__ = "lehrer"
>>>>>>> f11c925 (Versuch Server Push)

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

<<<<<<< HEAD
    KlassenID = db.Column(
        db.String(36),
        db.ForeignKey("Klassen.id"),
        nullable=False
    )

    def __init__(self, name, nachname, KlassenID):
        self.name = name
        self.nachname = nachname
        self.KlassenID = KlassenID

def erstellung(mail, password, name, nachname, klasse):
    user = User(
        mail=mail.strip().lower(),
        password=crypting1.pasoschlsl(password),
=======
    Unterichtid = db.Column(
        db.String(36),
        db.ForeignKey("Fach.id"),
        nullable=False
    )

def erstellung(mail, password, name, nachname, klasse=None):
    user = User(
        mail=mail.strip().lower(),
        password=crypting.pasoschlsl(password),
>>>>>>> f11c925 (Versuch Server Push)
        name=name,
        nachname=nachname,
        KlassenID=klasse,
        last_log=datetime.now(timezone.utc),
        online=True,
        trys=0,
    )

    db.session.add(user)
    db.session.commit()
    return user

<<<<<<< HEAD
def personal_erstellung(name, nachname, KlassenID):
    user = Personal(
        name=name,
        nachname=nachname,
        KlassenID=KlassenID
    )

    db.session.add(user)
    db.session.commit()
    return user

def Klassenerstellung(klasse, fachname):
    user = Klassen(
        Klasse=klasse,
        fachname=fachname
    )   

    db.session.add(user)
    db.session.commit()
    return user
def userfach_erstellung(user_id, fach_id):
    user = HelferSchuler(
=======
def lehrer_erstellung(name, nachname, unterichtid):
    lehrer = Lehrer(
        name=name,
        nachname=nachname,
        Unterichtid=unterichtid
    )

    db.session.add(lehrer)
    db.session.commit()
    return lehrer

def fach_erstellung(fachname):
    fach = Fach(
        fachname=fachname
    )

    db.session.add(fach)
    db.session.commit()
    return fach

def userfach_erstellung(user_id, fach_id):
    userfach = UserFach(
>>>>>>> f11c925 (Versuch Server Push)
        user_id=user_id,
        fach_id=fach_id
    )

<<<<<<< HEAD
    db.session.add(user)
    db.session.commit()
    return user

def termin_erstellung(beuzugsdaten, date, standpunkt):
    user = Termin(
=======
    db.session.add(userfach)
    db.session.commit()
    return userfach

def termin_erstellung(beuzugsdaten, date, standpunkt):
    termin = Termin(
>>>>>>> f11c925 (Versuch Server Push)
        beuzugsdaten=beuzugsdaten,
        date=date,
        standpunkt=standpunkt
    )

<<<<<<< HEAD
    db.session.add(user)
    db.session.commit()
    return user
=======
    db.session.add(termin)
    db.session.commit()
    return termin
>>>>>>> f11c925 (Versuch Server Push)


def suche(wow):
    email_clean = str(wow or "").strip().lower()
    return User.query.filter_by(mail=email_clean).first()


def idsuche(wow):
    return User.query.filter_by(name=wow).scalar()
