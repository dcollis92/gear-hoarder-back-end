import os

DATABASE_URL = os.getenv('DATABASE_URL')

class Config:
  SQLALCHEMY_ECHO = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = DATABASE_URL
  if 'ON_HEROKU' in os.environ:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("://", "ql://", 1)