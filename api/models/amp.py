from datetime import datetime
from api.models.db import db

class Amp(db.Model):
    __tablename__ = 'amps'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column('type', db.Enum('Combo', 'Head', 'Cabinet', 'Power Amp', 'Pre-Amp', name='type'))
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    wattage = db.Column(db.Integer)
    speaker_size = db.Column(db.Integer)
    speaker_amount = db.Column(db.Integer)
    power_type = db.Column('power_type', db.Enum('Tube', 'Solid State', 'Hybrid', name='power_type'))
    ohm_rating = db.Column('ohm_rating', db.Enum('4', '8', '16', 'Multi',  name='ohm_rating'))
    color = db.Column(db.String(100))
    year = db.Column(db.String(4))
    description = db.Column(db.String(250))
    is_working = db.Column(db.Boolean, default=True, nullable=False)
    on_loan = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    
    def __repr__(self):
      return f"Amp('{self.id}', '{self.make}', '{self.model}', '{self.type}'"
      
    def serialize(self):
      amp = {a.name: getattr(self, a.name) for a in self.__table__.columns}
      return amp