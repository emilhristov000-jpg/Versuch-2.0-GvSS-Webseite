import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    rolle = db.Column(
       db.String(12),
       nullable=True
    )

    position = db.Column(
        db.String(12),
        nullable=True
    )

    mail = db.Column(
        db.String(50),
        nullable=False
    )

    Bestanden = db.Column(
        db.Boolean,
        nullable=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    topt = db.Column(
        db.String(6),
        nullable=True
    )

    name = db.Column(
        db.String(20),
        nullable=False
    )

    nachname = db.Column(
        db.String(30),
        nullable=False
    )

    Klassen = db.Column(
        db.String(20),
        nullable=True
    )




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

    def __init__(self, **kwargs):
        self.fachname = kwargs.get("fachname")


class Termin(db.Model):
    __tablename__ = "termine"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    Helfer = db.Column(
        db.String(36),
        db.ForeignKey("User.id"),
        nullable=False
    )

    erhalter = db.Column(
        db.String(36),
        db.ForeignKey("User.id"),
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


def erstellung(mail, password, name, nachname, klasse=None, rolle=None, position=None,Bestanden=None):
    user = User(
        mail=mail,
        password=password,
        name=name,
        nachname=nachname,
        Klassen=klasse,
        rolle=rolle,
        position=position,
        Bestanden=Bestanden
    )
    db.session.add(user)
    db.session.commit()
    return user


def fach_erstellung(fachname):
    fach = Fach(fachname=fachname)
    db.session.add(fach)
    db.session.commit()
    return fach


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
