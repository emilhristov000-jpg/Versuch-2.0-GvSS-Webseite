from py_Folder import redus,slq
from py_Folder.slq import db
from flask import Flask,render_template, request, redirect, session
import bleach
import os


redus.redis_start()
app = Flask(__name__)


with open("geheim.key", "r") as apl:
    app.secret_key = apl.read()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///Schüler_Helfen_Schüler.db"
)
#slq.erstellung(str("JuStMonika@gmail.com").strip().lower(), "Monika", "Monika", "Monika")


db.init_app(app)

@app.route('/', methods=['GET','POST'])
def anmelde():
    nmeld = request.form.get("mail")
    pmeld = request.form.get("paso")
    numeld = slq.suche(nmeld)
    wow= slq.idsuche(nmeld)
    

    if request.method == 'POST':
        if numeld and nmeld and slq.crypting.check_password_hash(numeld.password,pmeld):
            session["id"] = numeld.id
            return  redirect("/wo")
        else :
            return render_template('startseite.html',error="Fehlerhafter Versuch")

    return render_template('startseite.html')

@app.route('/wo', methods=['GET','POST'])
def wo():
    return render_template('login_a.html')
if __name__ == '__main__':  
    app.run(host='0.0.0.0', debug=True)