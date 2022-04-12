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
    