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
