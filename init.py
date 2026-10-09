<<<<<<< HEAD
from py_Folder import redus,slq,crypting1
=======
from py_Folder import redus, slq, crypting
>>>>>>> f11c925 (Versuch Server Push)
from py_Folder.slq import db, erstellung
from flask import Flask, render_template, request, redirect, session, abort
import os
import secrets
from flask_admin import Admin
<<<<<<< HEAD
=======
from flask_admin.theme import Bootstrap4Theme
>>>>>>> f11c925 (Versuch Server Push)
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config['SECRET_KEY']= secrets.token_hex(32)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///Schüler_Helfen_Schüler.db",
)

db.init_app(app)




@app.route("/", methods=["GET", "POST"])
def anmelde():
    if request.method == "POST":
        nmeld = request.form.get("mail", "").strip().lower()
        pmeld = request.form.get("paso", "")

        numeld = slq.suche(nmeld)

<<<<<<< HEAD
        if numeld and crypting1.check_password_hash(numeld.password, pmeld):
=======
        if numeld and crypting.check_password_hash(numeld.password, pmeld):
>>>>>>> f11c925 (Versuch Server Push)
            session["id"] = numeld.id
            session["class_id"] = numeld.KlassenID
            return redirect("/wo")

        return render_template("startseite.html",error="Fehlerhafter Versuch",)

    return render_template("startseite.html")


@app.route("/wo", methods=["GET", "POST"])
def wo():
    fächer = ["Mathematik","Deutsch","Englisch","Chemie","Physik","Informatik","BWL","Reli/Ethik","VWL",]
    user_id = session.get("id")
    selected_fach_summ = 0
    selected_fach = [fach for fach in request.form.getlist("fach") if fach]

    if selected_fach:
        selected_fach_summ = sum(int(fach) for fach in selected_fach)

    if not user_id:
        return redirect("/")

    user = db.session.get(slq.User, user_id)

    if user is None:
        session.clear()
        return redirect("/")

    class_id = user.KlassenID

    if not class_id:
        return redirect("/")
    if request.method == "POST":

        for i in selected_fach:
            if i is not None:
                selected_fach_summ += int(i)
        if selected_fach:
            session["selected_fach"] = selected_fach
            return render_template("dashboard_fur_shs.html", user=user, fächer=fächer, class_id=class_id, selected_fach=selected_fach,selected_fach_summ=selected_fach_summ)
<<<<<<< HEAD

    return render_template("dashboard_fur_shs.html", user=user, fächer=fächer, class_id=class_id,selected_fach=selected_fach,selected_fach_summ=selected_fach_summ)

=======

    return render_template("dashboard_fur_shs.html", user=user, fächer=fächer, class_id=class_id,selected_fach=selected_fach,selected_fach_summ=selected_fach_summ)

@app.route("/admin")
def yobro__():
    return Admin(app,name="Al husein",theme=Bootstrap4Theme())
>>>>>>> f11c925 (Versuch Server Push)


#slq.erstellung("emo.He@gvss.de","password","emo","emo2","10A")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
#    redus.redis_start()
    app.run(host="0.0.0.0",port=8080,debug=True)