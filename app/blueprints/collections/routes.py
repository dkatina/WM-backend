from flask import request, jsonify
from app.models import Collection, db
from .schemas import collection_schema, collections_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import collections_bp

#Login

#Register/Create collection
@collections_bp.route('', methods=['POST'])
def create_collection():
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
        "collection": collection_schema.dump(new_collection)
    }), 201


#View Profile - Token Auth Eventually
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

#Update Profile
@collections_bp.route('/<int:collection_id>', methods=['PUT'])
def update_collection(collection_id):
    collection = db.session.get(Collection,collection_id)

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


#Delete Profile
@collections_bp.route('/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    collection = db.session.get(Collection, collection_id)
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return jsonify({"message": "successfully deleted collection."}), 200
    return jsonify({"error": "invalid collection id"}), 404
