from py_Folder import slq, crypting1
from init import app

with app.app_context():
    try:
        slq.db.drop_all()
        slq.db.create_all()
        user = slq.erstellung(
            "test@example.com",
            "password",
            "Test",
            "User",
            "10B",
        )
        print(f"Benutzer erstellt: {user.mail}, Klasse: {user.KlassenID}")
        print(f"Password valid: {crypting1.check_password_hash(user.password, 'password')}")
    except Exception as e:
        print(f"Error occurred: {e}")