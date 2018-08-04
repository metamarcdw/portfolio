import os
import json
from werkzeug.security import generate_password_hash
from server import secrets

secret_path = os.path.join(os.path.dirname(__file__), "secrets.json")
new_password = input("Enter a new password: ")
secrets["password_hash"] = generate_password_hash(new_password)
with open(secret_path, "w") as ofile:
    json.dump(secrets, ofile, indent=4)
