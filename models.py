from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Enum as SAEnum
import enum
from app import db  

class ShipmentStatus(enum.Enum):
    pending = "Pending"
    in_transit = "In-Transit"
    delivered = "Delivered"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pw_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Shipment(db.Model):
    __tablename__ = "shipments"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)               
    status = db.Column(SAEnum(ShipmentStatus), nullable=False, default=ShipmentStatus.pending) 
    is_fragile = db.Column(db.Boolean, nullable=False, default=False) 

    # 3 input fields
    base_cost = db.Column(db.Float, nullable=False, default=0.0)   
    tax_rate = db.Column(db.Float, nullable=False, default=0.0)   
    handling_fee = db.Column(db.Float, nullable=False, default=0.0) 

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def total_cost(self):
        """Calculated field derived from base_cost, tax_rate and handling_fee."""
        try:
            # total = base_cost + tax_amount + handling_fee
            # tax_amount = base_cost * tax_rate
            return round(self.base_cost * (1 + float(self.tax_rate)) + float(self.handling_fee), 2)
        except Exception:
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value if self.status else None,
            "is_fragile": self.is_fragile,
            "base_cost": self.base_cost,
            "tax_rate": self.tax_rate,
            "handling_fee": self.handling_fee,
            "total_cost": self.total_cost,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }