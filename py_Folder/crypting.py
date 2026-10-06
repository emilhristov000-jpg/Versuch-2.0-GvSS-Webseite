from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.security import check_password_hash
schlslkey_ = "geheim.key"
if os.path.exists(schlslkey_):
    with open(schlslkey_,"rb") as f:
        frnt_schlsl = f.read()
else:
    frnt_schlsl = Fernet.generate_key()
    with open(schlslkey_,"wb") as f:
        f.write(frnt_schlsl)
freenet = Fernet(frnt_schlsl)

def schlsl(wow):

    return freenet.encrypt(str(wow).encode()).decode()

def entschlsl(wow):
    try:
        return freenet.decrypt(str(wow).encode()).decode()
    except Exception:
        return wow


def pasoschlsl(wow):
    return generate_password_hash(str(wow))