from py_Folder import redus, slq, crypting1
from py_Folder.slq import db
from flask import Flask, render_template, request, redirect, session
import os
import secrets
from flask_admin import AdminIndexView, expose,Admin,BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme


app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(32)

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

        if numeld and crypting1.check_password_hash(numeld.password, pmeld):
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

    return render_template("dashboard_fur_shs.html", user=user, fächer=fächer, class_id=class_id,selected_fach=selected_fach,selected_fach_summ=selected_fach_summ)



class adminprobe(AdminIndexView):
    def is_accessible(self):
        return True #session.get('user_role') == 'admin'

    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')


admin = Admin(app,url="/admin", theme=Bootstrap4Theme(swatch='darkly'), index_view=adminprobe())



class neuecostumseite(BaseView):
    @expose('/')
    def neuecostumseite(self):
        return self.render('admin/index.html')

    @expose('/details/')
    def details(self):
        return self.render('admin/daten_details.html')

admin.add_views(neuecostumseite (name='Versuch2', endpoint='custom'),
                ModelView(slq.User,db.session,name="Benutzer"),
                ModelView(slq.Klassen,db.session,name="Klassen"),
                ModelView(slq.Fach,db.session,name="Fächer"),
                ModelView(slq.HelferSchuler,db.session,name="HelferSchuler"),
                ModelView(slq.Termin, db.session,name="Termine"),
                ModelView(slq.Lehrer, db.session, name="Lehr kräfte"))
#slq.erstellung("emo.He@gvss.de","password","emo","emo2","10A")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
#    redus.redis_start()
    app.run(host="0.0.0.0",port=8080,debug=True)