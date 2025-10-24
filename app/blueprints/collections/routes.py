from flask import request, jsonify
from app.models import Collection, db, User
from app.util.auth import token_required
from .schemas import collection_schema, collections_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import collections_bp


#Login

#Register/Create collection
@collections_bp.route('', methods=['POST'])
@token_required
def create_collection():
    user = db.session.get(User, request.user_id)

    if len(user.collections) >= 5:
        return jsonify({'error': 'You have reach the maximum stored albums'}), 400
    

    #load validata the request data
    try:
        data = collection_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    
    new_collection = Collection(**data) #Create new collection
    db.session.add(new_collection)
    db.session.commit()
    #create a new collection in my database

    

    #send a response
    return jsonify({
        "message": "successfully create collection",
        "collections": collections_schema.dump(user.collections)
    }), 201


#View Collection - Token Auth Eventually
@collections_bp.route('/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    collection = db.session.get(Collection, collection_id)
    if collection: 
        return collection_schema.jsonify(collection), 200
    return jsonify({"error": "invalid collection id"}), 400

#View All collections
@collections_bp.route('', methods=['GET'])
def get_collections():
    collections = db.session.query(Collection).all()
    return collections_schema.jsonify(collections), 200

#Update Collection
@collections_bp.route('/<int:collection_id>', methods=['PUT'])
@token_required
def update_collection(collection_id):
    collection = db.session.get(Collection,collection_id)
    user_id = request.user_id
    if user_id != collection.user_id:
        return jsonify({"error": "access denied"})

    if not collection:
        return jsonify({"error": "Invalid collection Id"}), 404
    
    try:
        data = collection_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in data.items():
        setattr(collection, key, value)

    db.session.commit()
    return jsonify({
        "message": "successfully upadated account",
        "collection": collection_schema.dump(collection)
    }), 200


#Delete Collection
@collections_bp.route('/<int:collection_id>', methods=['DELETE'])
@token_required
def delete_collection(collection_id):
    collection = db.session.get(Collection, collection_id)
    user_id = request.user_id
    user = db.session.get(User, user_id)
    if user_id != collection.user_id:
        return jsonify({"error": "access denied"})
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return jsonify({
            "message": "successfully deleted collection.",
            "collections": collections_schema.dump(user.collections)}), 200
    return jsonify({"error": "invalid collection id"}), 404
