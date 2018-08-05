import sys
from getpass import getpass
from werkzeug.security import generate_password_hash
from server import create_app, db
from server.models import User

username = input("Enter your username: ")
new_password = getpass("Enter a new password: ")
match_pass = getpass("Re-enter new password: ")
assert new_password == match_pass, "Did not match."

# pylint: disable=E1101
with create_app().app_context():
    admin = User.query.filter_by(username=username).first()
    if not admin:
        yorn = input(f"Superuser '{username}' not found, create? [Y/N]: ")
        if yorn in ("Y", "y"):
            admin = User(username=username, password_hash="")
            db.session.add(admin)
        else:
            sys.exit(0)
    admin.password_hash = generate_password_hash(new_password)
    db.session.commit()
