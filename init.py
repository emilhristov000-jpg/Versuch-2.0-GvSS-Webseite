from py_Folder import redus,crypting
from flask import Flask,render_template, request, redirect, session


app = Flask(__name__)
crypting.strtcrypting()
redus.redis_start()
print(crypting.schlsl("WOW"))
print(crypting.entschlsl(crypting.schlsl("WOW")))

@app.route('/', methods=['GET','POST'])
def anmelde():
    return render_template('startseite.html')
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login_a.html')
if __name__ == '__main__':  
    app.run(host='0.0.0.0', debug=True, port=5000)