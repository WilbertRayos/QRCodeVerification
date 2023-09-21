from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import mysql.connector

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    passwd = db.Column(db.String(250))

class CSSR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_number = db.Column(db.String(250), nullable=False)
    ship_name = db.Column(db.String(250), nullable=False)
    distinctive_number = db.Column(db.String(250), nullable=False)
    port_of_registry = db.Column(db.String(250), nullable=False)
    gross_tonnage = db.Column(db.String(250), nullable=False)
    sea_areas = db.Column(db.String(250), nullable=False)
    imo_number = db.Column(db.String(250), nullable=False)
    valid_until = db.Column(db.DateTime(timezone=True))
    qr_text = db.Column(db.String(250), nullable=False, unique=True)

class SSLSES(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stats = db.Column(db.String(50), nullable=False)
    certificate_number = db.Column(db.String(250), nullable=False)
    ship_name = db.Column(db.String(250), nullable=False)
    call_sign = db.Column(db.String(250), nullable=False)
    imo_number = db.Column(db.String(250), nullable=False)
    aaic = db.Column(db.String(250), nullable=False)
    class_type = db.Column(db.String(250), nullable=False)
    ship_owner = db.Column(db.String(250), nullable=False)
    qr_text = db.Column(db.String(250), nullable=False, unique=True)