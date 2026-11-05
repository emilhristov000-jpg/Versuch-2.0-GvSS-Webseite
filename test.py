from py_Folder import slq
from init import app

with app.app_context():
    try:
        slq.db.drop_all()
        slq.db.create_all()
        user = slq.erstellung(
            "123@a.com",
            "123",
            "Test",
            "User",
            "10B",
        )
        print(f"Benutzer erstellt: {user.mail}, Klasse: {user.Klassen}")
        print(f"Password valid: {user.password, 'password'}")
    except Exception as e:
        print(f"Error occurred: {e}")