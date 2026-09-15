from py_Folder import slq
from init import app


with app.app_context():
    try:
        user = slq.erstellung(
            "test@example.com",
            "password",
            "Test",
            "User",
            "10B",
        )
        print(f"Benutzer erstellt: {user.mail}, Klasse: {user.klasse}")

    except Exception as e:
        print(f"Error occurred: {e}")