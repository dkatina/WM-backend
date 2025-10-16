from flask import request, jsonify
from app.models import User, db
from app.util.auth import encode_token, token_required
from .schemas import user_schema, users_schema, login_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp

#Login
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.json) #unpacking email and password
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user = db.session.query(User).where(User.email == data['email']).first() #checking if a user belongs to this email

    if user and check_password_hash(user.password, data['password']): #If we found a user with that email, then check that users email against the email that was passed in
        token = encode_token(user.id, user.role)
        return jsonify({
            "message": "Successfully logged in",
            "token": token,
            "user": user_schema.dump(user)
        }), 200
    
    return jsonify({'error': 'invalid email or password'}), 404


#Register/Create User
@users_bp.route('', methods=['POST'])
def create_user():
    #load validata the request data
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    data['password'] = generate_password_hash(data['password']) #Reassigning the password to the hashed version of the pw

    user = db.session.query(User).where(User.email == data['email']).first() #Checking if a user exist in my db who has the same password as the one passed in
    if user:
        return jsonify({'error': 'Email already taken.'}), 400
    
    new_user = User(**data) #Create new user
    db.session.add(new_user)
    db.session.commit()
    #create a new User in my database

    #send a response
    return jsonify({
        "message": "successfully create user",
        "user": user_schema.dump(new_user)
    }), 201


#View Profile - Token Auth Eventually
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user: 
        return user_schema.jsonify(user), 200
    return jsonify({"error": "invalid user id"}), 400

#View All Users
@users_bp.route('', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return users_schema.jsonify(users), 200

#Update Profile
@users_bp.route('', methods=['PUT'])
@token_required
def update_user():
    user_id = request.user_id #grabbing the user id from the request
    user = db.session.get(User,user_id)

    if not user:
        return jsonify({"error": "Invalid User Id"}), 404
    
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password'] = generate_password_hash(data['password'])

    existing = db.session.query(User).where(User.email == data['email']).first()
    if existing:
        return jsonify({"error": "Email already taken."})

    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    return jsonify({
        "message": "successfully upadated account",
        "user": user_schema.dump(user)
    }), 200


#Delete Profile
@users_bp.route('', methods=['DELETE'])
@token_required
def delete_user():
    user_id = request.user_id
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "successfully deleted user."}), 200
    return jsonify({"error": "invalid user id"}), 404
