from py_Folder import redus, slq
from py_Folder.slq import db, erstellung
from flask import Flask, render_template, request, redirect, session, abort
import os


app = Flask(__name__)

with open("geheim.key", "r") as apl:
    app.secret_key = apl.read()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///Schüler_Helfen_Schüler.db",
)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def anmelde():
    if request.method == "POST":
        nmeld = request.form.get("mail", "").strip().lower()
        pmeld = request.form.get("paso", "")

        numeld = slq.suche(nmeld)

        if numeld and slq.crypting.check_password_hash(
            numeld.password,
            pmeld,
        ):
            session["id"] = numeld.id
            session["class_id"] = numeld.klasse
            return redirect("/wo")

        return render_template("startseite.html",error="Fehlerhafter Versuch",)

    return render_template("startseite.html")


@app.route("/wo", methods=["GET", "POST"])
def wo():
    user_id = session.get("id")

    if not user_id:
        return redirect("/")

    user = db.session.get(slq.User, user_id)

    if user is None:
        session.clear()
        return redirect("/")

    class_id = user.klasse

    if not class_id:
        return redirect("/")

    fächer = ["Mathematik","Deutsch","Englisch","Chemie","Physik","Informatik","BWL","Reli/Ethik","VWL",]

    return render_template("dashboard_fur_shs.html", user=user, fächer=fächer, class_id=class_id,)




if __name__ == "__main__":
    redus.redis_start()
    app.run(host="0.0.0.0",debug=True,use_reloader=False,)