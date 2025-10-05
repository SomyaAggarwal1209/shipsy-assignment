import pytest
from app import app, db, Shipment
from app import Shipment as ShipmentModel  

@pytest.fixture(scope="module")
def test_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def create_shipment(base_cost, tax_rate, handling_fee):
    s = Shipment(
        description="test",
        base_cost=base_cost,
        tax_rate=tax_rate,
        handling_fee=handling_fee
    )
    db.session.add(s)
    db.session.commit()
    return s

def test_total_cost_zero_values(test_app):
    s = create_shipment(0.0, 0.0, 0.0)
    assert s.total_cost == 0.0

def test_total_cost_fractional_tax(test_app):
    s = create_shipment(100.0, 0.18, 5.0)  # base 100, tax 18, handling 5 => 100*1.18 + 5 = 123.0
    assert s.total_cost == 123.0

def test_total_cost_large_values(test_app):
    s = create_shipment(1_000_000.0, 0.12, 200.0)
    expected = round(1_000_000.0 * (1 + 0.12) + 200.0, 2)
    assert s.total_cost == expected

# def test_total_cost_non_numeric_returns_none(test_app):
#     s = Shipment(description="bad", base_cost=None, tax_rate=None, handling_fee=None)
#     db.session.add(s)
#     db.session.commit()
#     assert s.total_cost is None
