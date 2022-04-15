from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.amp import Amp

amps = Blueprint('amps', 'amps')

# Create Amp
@amps.route('/', methods=["POST"])
@login_required
def create():
    data = request.get_json()
    print(data)
    profile = read_token(request)
    data["profile_id"] = profile["id"]
    amp = Amp(**data)
    db.session.add(amp)
    db.session.commit()
    return jsonify(amp.serialize()), 201

# Index Amps
@amps.route('/', methods=["GET"])
def index():
  amps = Amp.query.all()
  return jsonify([amp.serialize() for amp in amps]), 200

# Show Amp
@amps.route('/<id>', methods=["GET"])
def show(id):
  amp = Amp.query.filter_by(id=id).first()
  amp_data = amp.serialize()
  return jsonify(amp=amp_data), 200

# Update Amp
@amps.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  amp = Amp.query.filter_by(id=id).first()

  if amp.profile_id != profile["id"]:
    return 'Sorry, bubba', 403
  
  for key in data:
    setattr(amp, key, data[key])
  
  db.session.commit()
  return jsonify(amp.serialize()), 200

# Delete Amp
@amps.route('<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  amp = Amp.query.filter_by(id=id).first()

  if amp.profile_id != profile["id"]:
    return 'Get outta town!', 403
  
  db.session.delete(amp)
  db.session.commit()
  return jsonify(message="Success"), 200

@amps.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500