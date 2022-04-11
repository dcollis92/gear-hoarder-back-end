from datetime import datetime
from api.models.db import db

class Rig(db.Model):
    __tablename__ = 'rigs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Rig('{self.id}', '{self.name}'"

    def serialize(self):
      rig = {r.name: getattr(self, r.name) for r in self.__table__.columns}
      return rig