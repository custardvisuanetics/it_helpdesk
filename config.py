import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "change-this-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "helpdesk.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
