from werkzeug.security import generate_password_hash, check_password_hash

def password_hash(password):
   return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(entered_password, valid_password):
    return check_password_hash(valid_password, entered_password)