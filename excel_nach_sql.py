import pandas as pd
from faker import Faker

from init import app
from py_Folder.slq import db,erstellung

faker = Faker('de_DE')


with app.app_context():
    db.create_all()
 
    df = pd.read_excel("Projektarbeit_anonymisiert.xlsx", header=None)
    wow = df.values.tolist()

    for i in wow:
        mail = f"{i[2]}.{i[3]}@gvss.de"
        mail = mail.replace(" ","").strip().lower()
        erstellung(mail, faker.password(), i[3], i[2], i[0], "Schüler", "", None)