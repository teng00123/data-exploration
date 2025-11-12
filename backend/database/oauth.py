from datetime import datetime
from backend.config import db


class ClientUserInfo(db.Model):
    __tablename__ = 'client_user_info'
    client_id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.BigInteger)

class ClientSecretInfo(db.Model):
    __tablename__ = 'client_secret_info'
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)
    is_disable = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

