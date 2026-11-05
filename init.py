import os
import secrets

from flask import Flask, redirect, render_template, request, session
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme

from py_Folder import slq
from py_Folder.slq import db, fach_erstellung



app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(32)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///Schüler_Helfen_Schüler.db",
)

db.init_app(app)

schluessel_datei = "geheim.key"
if os.path.exists(schluessel_datei):
    with open(schluessel_datei, "rb") as datei:
        schluessel = datei.read()
else:
    schluessel = secrets.token_hex(32).encode("utf-8")
    with open(schluessel_datei, "wb") as datei:
        datei.write(schluessel)

@app.route("/", methods=["GET", "POST"])
def anmeldung():
    if request.method == "POST":
        email = request.form.get("mail", "").strip().lower()
        passwort = request.form.get("paso", "")

        benutzer = slq.suche(email)

        if benutzer and benutzer.password == passwort:
            session["id"] = benutzer.id
            session["class_id"] = benutzer.Klassen
            session["user_role"] = benutzer.rolle
            return redirect("/wo")

        return render_template("startseite.html", error="Fehlerhafter Versuch")

    return render_template("startseite.html")


@app.route("/wo", methods=["GET", "POST"])
def wo():
    fächer = ["Mathe","Deutsch","English","BWL","DVA","Physik"]
    if request.method == "POST":
        nutzerid = session.get("id")
        if nutzerid:
            for fach in request.form.getlist("fach"):
                fach_erstellung(fach, nutzerid)
    return render_template("dashboard_fur_shs.html",fächer=fächer)



class AdminProbe(AdminIndexView):
    def is_accessible(self):
        return True  # session.get("user_role") == "admin"

    
    def inaccessible_callback(self, name, **kwargs):
        return redirect("/")


admin = Admin(
    app,
    url="/admin",
    theme=Bootstrap4Theme(swatch="darkly"),
    index_view=AdminProbe(),
)



class adminprobe(BaseView):
    @expose('/')
    def neue_custom_seite(self):
        return self.render('admin/index.html')

    @expose('/details/')
    def details(self):
        return self.render('admin/daten_details.html')

admin.add_views(
    adminprobe(name="Versuch2", endpoint="custom"),
    ModelView(slq.User, db, name="Benutzer"),
    ModelView(slq.Fach, db, name="Fächer"),
    ModelView(slq.Termin, db, name="Termine"),
)
# slq.erstellung("emo.He@gvss.de", "password", "emo", "emo2", "10A")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)