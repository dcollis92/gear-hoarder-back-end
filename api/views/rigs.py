from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.rig import Rig

rigs = Blueprint('rigs', 'rigs')

@rigs.route('/', methods=["POST"])
@login_required
def create():
    data = request.get_json()
    profile = read_token(request)
    data["profile_id"] = profile["id"]
    rig = Rig(**data)
    db.session.add(rig)
    db.session.commit()
    return jsonify(rig.serialize()), 201

@rigs.route('/', methods=["GET"])
def index():
  rigs = Rig.query.all()
  return jsonify([rig.serialize() for rig in rigs]), 200

@rigs.route('/<id>', methods=["GET"])
def show(id):
  rig = Rig.query.filter_by(id=id).first()
  rig_data = rig.serialize()
  return jsonify(rig=rig_data), 200

@rigs.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  rig = Rig.query.filter_by(id=id).first()

  if rig.profile_id != profile["id"]:
    return 'Sorry, bubba', 403
  
  for key in data:
    setattr(rig, key, data[key])
  
  db.session.commit()
  return jsonify(rig.serialize()), 200
