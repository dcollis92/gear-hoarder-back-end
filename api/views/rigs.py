from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.rig import Rig
from api.models.guitar import Guitar
from api.models.amp import Amp
from api.models.pedal import Pedal
from api.models.association import Association

rigs = Blueprint('rigs', 'rigs')

# Create Rigs
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

# Index Rigs
@rigs.route('/', methods=["GET"])
def index():
  rigs = Rig.query.all()
  return jsonify([rig.serialize() for rig in rigs]), 200

# Show Rig
@rigs.route('/<id>', methods=["GET"])
def show(id):
  rig = Rig.query.filter_by(id=id).first()
  rig_data = rig.serialize()
  # Gear Association
  guitars = Guitar.query.filter(Guitar.id.notin_([guitar.id for guitar in rig.guitars])).all()
  guitars=[guitar.serialize() for guitar in guitars]
  amps = Amp.query.filter(Amp.id.notin_([amp.id for amp in rig.amps])).all()
  amps=[amp.serialize() for amp in amps]
  pedals = Pedal.query.filter(Pedal.id.notin_([pedal.id for pedal in rig.pedals])).all()
  pedals=[pedal.serialize() for pedal in pedals]

  return jsonify(rig=rig_data, available_pedals=pedals, available_amps=amps, available_guitars=guitars), 200

# Update Rig
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

# Delete Rig
@rigs.route('<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  rig = Rig.query.filter_by(id=id).first()

  if rig.profile_id != profile["id"]:
    return 'Get outta town!', 403
  
  db.session.delete(rig)
  db.session.commit()
  return jsonify(message="Success"), 200

# Associate Guitar
@rigs.route('/<rig_id>/guitars/<guitar_id>', methods=["LINK"]) 
@login_required
def assoc_guitar(rig_id, guitar_id):
  data = { "rig_id": rig_id, "guitar_id": guitar_id }

  profile = read_token(request)
  rig = Rig.query.filter_by(id=rig_id).first()
  
  if rig.profile_id != profile["id"]:
    return 'Forbidden', 403

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  rig = Rig.query.filter_by(id=rig_id).first()
  return jsonify(rig.serialize()), 201

# Associate Amp
@rigs.route('/<rig_id>/amps/<amp_id>', methods=["LINK"]) 
@login_required
def assoc_amp(rig_id, amp_id):
  data = { "rig_id": rig_id, "amp_id": amp_id }

  profile = read_token(request)
  rig = Rig.query.filter_by(id=rig_id).first()
  
  if rig.profile_id != profile["id"]:
    return 'Forbidden', 403

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  rig = Rig.query.filter_by(id=rig_id).first()
  return jsonify(rig.serialize()), 201

#Associate Pedal
@rigs.route('/<rig_id>/pedals/<pedal_id>', methods=["LINK"]) 
@login_required
def assoc_pedal(rig_id, pedal_id):
  data = { "rig_id": rig_id, "pedal_id": pedal_id }

  profile = read_token(request)
  rig = Rig.query.filter_by(id=rig_id).first()
  
  if rig.profile_id != profile["id"]:
    return 'Forbidden', 403

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  rig = Rig.query.filter_by(id=rig_id).first()
  return jsonify(rig.serialize()), 201

@rigs.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500