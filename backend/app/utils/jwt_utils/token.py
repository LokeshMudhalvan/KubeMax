from flask_jwt_extended import create_access_token, get_jwt_identity

def generate_token(user_id):
    return create_access_token(user_id)

def get_user_id():
    return get_jwt_identity()