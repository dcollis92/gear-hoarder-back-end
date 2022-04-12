from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.pedal import Pedal

pedals = Blueprint('pedals', 'pedals')

# Create Pedal
@pedals.route('/', methods=["POST"])
@login_required
def create():
    data = request.get_json()
    profile = read_token(request)
    data["profile_id"] = profile["id"]
    pedal = Pedal(**data)
    db.session.add(pedal)
    db.session.commit()
    return jsonify(pedal.serialize()), 201

# Index Pedals 
@pedals.route('/', methods=["GET"])
def index():
  pedals = Pedal.query.all()
  return jsonify([pedal.serialize() for pedal in pedals]), 200

# Show Pedal
@pedals.route('/<id>', methods=["GET"])
def show(id):
  pedal = Pedal.query.filter_by(id=id).first()
  pedal_data = pedal.serialize()
  return jsonify(pedal=pedal_data), 200

# Update Pedal
@pedals.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  pedal = Pedal.query.filter_by(id=id).first()

  if pedal.profile_id != profile["id"]:
    return 'Sorry, bubba', 403
  
  for key in data:
    setattr(pedal, key, data[key])
  
  db.session.commit()
  return jsonify(pedal.serialize()), 200

# Delete Pedal
@pedals.route('<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  pedal = Pedal.query.filter_by(id=id).first()

  if pedal.profile_id != profile["id"]:
    return 'Get outta town!', 403
  
  db.session.delete(pedal)
  db.session.commit()
  return jsonify(message="Success"), 200

@pedals.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500