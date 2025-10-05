
from app import app, db, Shipment
from datetime import datetime, timezone
with app.app_context():
    # fresh in-memory DB used by tests; but we will recreate tables to be safe
    db.drop_all()
    db.create_all()
    # create a shipment with explicit None values
    s = Shipment(description="bad", base_cost=None, tax_rate=None, handling_fee=None)
    db.session.add(s)
    db.session.commit()
    s = Shipment.query.get(s.id)
    print("base_cost:", s.base_cost, type(s.base_cost))
    print("tax_rate:", s.tax_rate, type(s.tax_rate))
    print("handling_fee:", s.handling_fee, type(s.handling_fee))
    print("total_cost:", s.total_cost, type(s.total_cost))

