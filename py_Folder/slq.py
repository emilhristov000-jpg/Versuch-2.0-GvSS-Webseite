from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

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

    trys = db.Column(
       db.Integer,
       default=0
    )

    rolle = db.Column(
       db.String(12),
       nullable=False,
       default="Sch?ler"
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
        nullable=True
    )

    def __init__(self, mail: str, password: str, name: str, nachname: str, KlassenID: str | None = None, last_log: datetime | None = None, online: bool = False, rolle: str | None = "Sch?ler", rolle2: str | None = ""):
        self.mail = str(mail or "").strip().lower()
        self.password = password
        self.name = str(name or "").strip()
        self.nachname = str(nachname or "").strip()
        self.KlassenID = KlassenID
        self.rolle = rolle or "Sch?ler"
        self.online = online
        if last_log is not None:
            self.last_log = last_log


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


class Fach(db.Model):
    __tablename__ = "fach"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    fachname = db.Column(
        db.String(25),
        nullable=False,
        unique=True
    )

    def __init__(self, fachname):
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
        db.ForeignKey("fach.id"),
        nullable=False
    )

    def __init__(self, user_id, fach_id):
        self.user_id = user_id
        self.fach_id = fach_id


UserFach = HelferSchuler


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

    def __init__(self,beuzugsdaten,date,standpunkt):
        self.bezugsdaten = beuzugsdaten,
        self.date = date,
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
        db.ForeignKey("fach.id"),
        nullable=False
    )


def erstellung(mail, password, name, nachname, klasse=None, rolle="Sch?ler", rolle2=""):
    user = User(
        mail=mail,
        password=password,
        name=name,
        nachname=nachname,
        KlassenID=klasse,
        rolle=rolle,
        rolle2=rolle2,
    )
    db.session.add(user)
    db.session.commit()
    return user


def Klassenerstellung(klasse, fachname):
    klasse_record = Klassen(Klasse=klasse, fachname=fachname)
    db.session.add(klasse_record)
    db.session.commit()
    return klasse_record


def fach_erstellung(fachname):
    fach = Fach(fachname=fachname)
    db.session.add(fach)
    db.session.commit()
    return fach


def userfach_erstellung(user_id, fach_id):
    userfach = UserFach(user_id=user_id, fach_id=fach_id)
    db.session.add(userfach)
    db.session.commit()
    return userfach


def termin_erstellung(beuzugsdaten, date, standpunkt):
    termin = Termin(
        beuzugsdaten=beuzugsdaten,
        date=date,
        standpunkt=standpunkt,
    )
    db.session.add(termin)
    db.session.commit()
    return termin


def suche(wow):
    email_clean = str(wow or "").strip().lower()
    return User.query.filter_by(mail=email_clean).first()


def idsuche(wow):
    return User.query.filter_by(name=wow).scalar()
