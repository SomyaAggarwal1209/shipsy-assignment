from app import db, Shipment, ShipmentStatus

def register_and_login(client, username="tester", password="pass123"):
    # Register user
    client.post("/register", data={"username": username, "password": password}, follow_redirects=True)
    # Login user
    resp = client.post("/login", data={"username": username, "password": password}, follow_redirects=True)
    assert resp.status_code == 200

def test_read_update_delete_shipment(test_client):
    client = test_client
    register_and_login(client)

    # CREATE manually in DB
    with client.application.app_context():
        s = Shipment(
            description="Integration Test Shipment",
            status=ShipmentStatus.pending,
            is_fragile=True,
            base_cost=100.0,
            tax_rate=0.18,
            handling_fee=5.0
        )
        db.session.add(s)
        db.session.commit()
        sid = s.id

    # READ
    resp = client.get("/shipments")
    assert resp.status_code == 200
    assert b"Integration Test Shipment" in resp.data

    # UPDATE
    edit_data = {
        "description": "Integration Test Shipment - Edited",
        "status": "Delivered",
        "base_cost": "150.00",
        "tax_rate": "0.10",
        "handling_fee": "2.50"
    }
    resp = client.post(f"/shipments/{sid}/edit", data=edit_data, follow_redirects=True)
    assert resp.status_code in (200, 302)
    with client.application.app_context():
        s2 = Shipment.query.get(sid)
        assert s2.description == "Integration Test Shipment - Edited"
        assert s2.status == ShipmentStatus.delivered

    # DELETE
    resp = client.post(f"/shipments/{sid}/delete", follow_redirects=True)
    assert resp.status_code in (200, 302)
    with client.application.app_context():
        assert Shipment.query.get(sid) is None