from py_Folder import slq
from init import app
from py_Folder import crypting1 


with app.app_context():
    try:
        user = slq.erstellung(
            "test@example.com",
            "password",
            "Test",
            "User",
            "10B",
        )
        print(f"Benutzer erstellt: {user.mail}, Klasse: {user.id}")

    except Exception as e:
        print(f"Error occurred: {e}")

a = [1, 2, 3,None, 5]
v = 0

for i in a:
    if i is not None:
        v += i
print(v) 