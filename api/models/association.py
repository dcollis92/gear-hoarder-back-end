from datetime import datetime
from api.models.db import db

class Association(db.Model):
    __tablename__ = 'associations'
    id = db.Column(db.Integer, primary_key=True)
    rig_id = db.Column(db.Integer, db.ForeignKey('rigs.id', ondelete='cascade'))
    guitar_id = db.Column(db.Integer, db.ForeignKey('guitars.id', ondelete='cascade'))
    amp_id = db.Column(db.Integer, db.ForeignKey('amps.id', ondelete='cascade'))
    pedal_id = db.Column(db.Integer, db.ForeignKey('pedals.id', ondelete='cascade'))