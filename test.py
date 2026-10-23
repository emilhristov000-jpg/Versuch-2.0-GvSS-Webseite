from py_Folder import slq
from init import app

with app.app_context():
    try:
        slq.db.drop_all()
        slq.db.create_all()
        user = slq.erstellung(
            "test@example.com",
            "test@example.com",
            "Test",
            "User",
            "10B",
        )
        print(f"Benutzer erstellt: {user.mail}, Klasse: {user.KlassenID}")
        print(f"Password valid: {user.password, 'password'}")
    except Exception as e:
        print(f"Error occurred: {e}")