from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Enum as SAEnum
import enum
from sqlalchemy import func
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

    # Allow NULL and no numeric default so None stays None when inserted
    base_cost = db.Column(db.Float, nullable=True, default=None)
    tax_rate = db.Column(db.Float, nullable=True, default=None)
    handling_fee = db.Column(db.Float, nullable=True, default=None)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    @property
    def total_cost(self):
        try:
            if self.base_cost is None or self.tax_rate is None or self.handling_fee is None:
                return None
            base = float(self.base_cost)
            tax = float(self.tax_rate)
            handling = float(self.handling_fee)
            return round(base * (1 + tax) + handling, 2)
        except (TypeError, ValueError):
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
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }