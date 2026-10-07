from init import app
from py_Folder.slq import Klassenerstellung
v = {
"Bfw" : ["Mathe", "Deutsch", "Englisch"],
"Bkwi" : ["Mathe","Deutsch","Eng"],
"Wg" : ["BWL", "Mathe"]
}
yo = []


with app.app_context():
    for klasse, fach in v.items():
        for fachi in fach:
            Klassenerstellung(klasse=klasse,fachname=fachi)