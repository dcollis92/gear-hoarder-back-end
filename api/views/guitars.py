from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.guitar import Guitar

guitars = Blueprint('guitars', 'guitars')

@guitars.route('/', methods=["POST"])
@login_required
def create():
    data = request.get_json()
    profile = read_token(request)
    data["profile_id"] = profile["id"]
    guitar = Guitar(**data)
    db.session.add(guitar)
    db.session.commit()
    return jsonify(guitar.serialize()), 201

@guitars.route('/', methods=["GET"])
def index():
  guitars = Guitar.query.all()
  return jsonify([guitar.serialize() for guitar in guitars]), 200

@guitars.route('/<id>', methods=["GET"])
def show(id):
  guitar = Guitar.query.filter_by(id=id).first()
  guitar_data = guitar.serialize()
  return jsonify(guitar=guitar_data), 200

@guitars.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  guitar = Guitar.query.filter_by(id=id).first()

  if guitar.profile_id != profile["id"]:
    return 'Sorry, bubba', 403
  
  for key in data:
    setattr(guitar, key, data[key])
  
  db.session.commit()
  return jsonify(guitar.serialize()), 200

@guitars.route('<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  guitar = Guitar.query.filter_by(id=id).first()

  if guitar.profile_id != profile["id"]:
    return 'Get outta town!', 403
  
  db.session.delete(guitar)
  db.session.commit()
  return jsonify(message="Success"), 200