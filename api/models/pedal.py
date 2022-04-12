from datetime import datetime
from api.models.db import db

# Add Association class here

class Pedal(db.Model):
    __tablename__ = 'pedals'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(100))
    year = db.Column(db.String(4))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
   
    def __repr__(self):
      return f"Pedal('{self.id}', '{self.make}', '{self.model}', '{self.type}'"
      
    def serialize(self):
      pedal = {p.name: getattr(self, p.name) for p in self.__table__.columns}
      return pedal